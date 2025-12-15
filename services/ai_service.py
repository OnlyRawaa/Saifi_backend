# services/ai_service.py
from __future__ import annotations

import logging
import math
import os
import pickle
import time
from typing import Any, Dict, List, Tuple

import numpy as np
from scipy.sparse import csr_matrix
from db.connection import get_connection
from services.ai_cache import STATE

logger = logging.getLogger("saifi.ai")

# ====== Config ======
MODEL_PATH = os.getenv("SAIFI_MODEL_PATH", "saifi_model.pkl")
CHILD_ENCODER_PATH = os.getenv("SAIFI_CHILD_ENCODER_PATH", "child_encoder.pkl")
ACTIVITY_ENCODER_PATH = os.getenv("SAIFI_ACTIVITY_ENCODER_PATH", "activity_encoder.pkl")

# refresh every N seconds (optional). set 0 to disable auto refresh checks.
REFRESH_TTL_SECONDS = int(os.getenv("SAIFI_AI_REFRESH_TTL_SECONDS", "0"))


# =========================
# Distance helper (safe)
# =========================
def calc_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    try:
        if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
            return 9999.0

        R = 6371.0
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)

        a = (math.sin(d_lat / 2) ** 2 +
             math.cos(math.radians(lat1)) *
             math.cos(math.radians(lat2)) *
             math.sin(d_lon / 2) ** 2)

        return 2 * R * math.asin(math.sqrt(a))
    except Exception:
        return 9999.0


# =========================
# Load model & encoders once
# =========================
def _load_pickle(path: str) -> Any:
    with open(path, "rb") as f:
        return pickle.load(f)


def load_assets_once() -> None:
    """Call this once at startup."""
    if STATE.model is not None and STATE.child_encoder and STATE.activity_encoder:
        return

    STATE.model = _load_pickle(MODEL_PATH)
    STATE.child_encoder = _load_pickle(CHILD_ENCODER_PATH)
    STATE.activity_encoder = _load_pickle(ACTIVITY_ENCODER_PATH)

    # ALS internal index -> UUID
    STATE.reverse_activity_map = {v: k for k, v in STATE.activity_encoder.items()}

    logger.info("AI assets loaded: model=%s children=%d activities=%d",
                type(STATE.model).__name__,
                len(STATE.child_encoder),
                len(STATE.activity_encoder))


# =========================
# Data loading + matrix build (cached)
# =========================

def fetch_all(query: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query)

    columns = [desc[0] for desc in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]

    cur.close()
    conn.close()
    return rows


async def refresh_ai_cache(force: bool = False) -> None:
    """
    Loads children/activities/bookings from DB and builds the sparse matrix once.
    This is the expensive part. Do it at startup, not per request.
    """
    # Optional TTL refresh
    if not force and REFRESH_TTL_SECONDS > 0:
        if time.time() - STATE.last_refresh_ts < REFRESH_TTL_SECONDS:
            return

    async with STATE.refresh_lock:
        # double-check inside lock
        if not force and REFRESH_TTL_SECONDS > 0:
            if time.time() - STATE.last_refresh_ts < REFRESH_TTL_SECONDS:
                return

        load_assets_once()

        # ---- fetch metadata ----
        children = fetch_all("""
            SELECT
                c.child_id::text AS child_id,
                EXTRACT(YEAR FROM AGE(c.birthdate))::int AS age,
                c.gender,
                c.interests,
                pr.location_lat AS lat,
                pr.location_lng AS lng
            FROM children c
            JOIN bookings b ON c.child_id = b.child_id
            JOIN providers pr ON b.provider_id = pr.provider_id
        """)

        
        activities = fetch_all("""
            SELECT
                a.activity_id::text AS activity_id,
                a.title AS activity_name,
                a.type AS category,
                a.price,
                a.duration AS duration_hours,
                a.age_from AS min_age,
                a.age_to AS max_age,
                pr.location_lat AS activity_lat,
                pr.location_lng AS activity_lng
            FROM activities a
            JOIN providers pr ON a.provider_id = pr.provider_id
        """)

        bookings = fetch_all("""
            SELECT child_id::text AS child_id, activity_id::text AS activity_id
            FROM bookings
            
        """)
        feedback = fetch_all("""
            SELECT
                child_id::text AS child_id,
                activity_id::text AS activity_id,
                rating,
                comment
            FROM feedback
            WHERE rating IS NOT NULL
        """)


        # build meta dicts
        STATE.child_meta = {
            r["child_id"]: {
                "age": r.get("age"),
                "gender": r.get("gender"),
                "interests": r.get("interests"),
                "lat": r.get("child_lat"),
                "lng": r.get("child_lng"),
            }
            for r in children
        }

        STATE.activity_meta = {
            r["activity_id"]: {
                "activity_name": r.get("activity_name"),
                "category": r.get("category"),
                "price": r.get("price"),
                "duration_hours": r.get("duration_hours"),
                "min_age": r.get("min_age"),
                "max_age": r.get("max_age"),
                "lat": r.get("activity_lat"),
                "lng": r.get("activity_lng"),
            }
            for r in activities
        }

        # ---- build popularity fallback ----
        # popularity: by avg rating then count (simple + effective)
        pop_stats: Dict[str, Tuple[float, int]] = {}  # activity_id -> (sum_rating, count)
        for b in bookings:
            aid = b["activity_id"]
            rt = float(b.get("rating", 0))
            s, c = pop_stats.get(aid, (0.0, 0))
            pop_stats[aid] = (s + rt, c + 1)

        # sort by (avg_rating desc, count desc)
        popular = sorted(
            pop_stats.items(),
            key=lambda kv: ((kv[1][0] / max(kv[1][1], 1)), kv[1][1]),
            reverse=True
        )
        # keep only activities that exist in meta (and have location if possible)
        STATE.popular_activity_ids = [
            aid for aid, _ in popular
            if aid in STATE.activity_meta
        ]

        # ---- build matrix ----
        if not bookings:
            # no ratings => no CF matrix; fallback only
            STATE.matrix = None
            STATE.last_refresh_ts = time.time()
            logger.warning("No bookings with ratings. Matrix not built; fallback will be used.")
            return

        child_encoder = STATE.child_encoder or {}
        activity_encoder = STATE.activity_encoder or {}

        # encode rows
        user_idx = []
        item_idx = []
        confidence = []

        alpha = 40.0

        for b in bookings:
            cid = b["child_id"]
            aid = b["activity_id"]
            r = b["rating"]

            if cid not in child_encoder or aid not in activity_encoder:
                continue
            if r is None:
                continue

            u = child_encoder[cid]
            i = activity_encoder[aid]
            conf = 1.0 + alpha * float(r)

            user_idx.append(u)
            item_idx.append(i)
            confidence.append(conf)

        if not user_idx:
            STATE.matrix = None
            STATE.last_refresh_ts = time.time()
            logger.warning("No encodable booking rows. Matrix not built; fallback will be used.")
            return

        user_idx = np.array(user_idx, dtype=np.int32)
        item_idx = np.array(item_idx, dtype=np.int32)
        confidence = np.array(confidence, dtype=np.float32)

        STATE.matrix = csr_matrix(
            (confidence, (user_idx, item_idx)),
            shape=(len(child_encoder), len(activity_encoder))
        )

        STATE.last_refresh_ts = time.time()
        logger.info(
            "AI cache refreshed: children=%d activities=%d ratings=%d matrix_nnz=%d",
            len(STATE.child_meta),
            len(STATE.activity_meta),
            len(user_idx),
            STATE.matrix.nnz if STATE.matrix is not None else 0
        )


# =========================
# Fallback recommendations (cold start)
# =========================
def _fallback_recommendations(child_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    child = STATE.child_meta.get(child_id, {})
    child_lat = child.get("lat") or 0.0
    child_lng = child.get("lng") or 0.0
    child_age = child.get("age")

    results = []

    # If we have popularity list, use it; else just any activities
    candidates = STATE.popular_activity_ids or list(STATE.activity_meta.keys())

    for aid in candidates:
        meta = STATE.activity_meta.get(aid)
        if not meta:
            continue

        # age filter if available
        min_age = meta.get("min_age")
        max_age = meta.get("max_age")
        if child_age is not None and min_age is not None and max_age is not None:
            try:
                if not (int(min_age) <= int(child_age) <= int(max_age)):
                    continue
            except Exception:
                pass

        dist = calc_distance(
            float(child_lat or 0.0),
            float(child_lng or 0.0),
            float(meta.get("lat") or 0.0),
            float(meta.get("lng") or 0.0),
        )

        results.append({
            "activity_id": aid,
            "activity_name": meta.get("activity_name"),
            "score": 0.0,  # fallback doesn't have CF score
            "distance_km": round(dist, 2),
            "category": meta.get("category"),
            "price": float(meta.get("price") or 0.0),
            "duration_hours": int(meta.get("duration_hours") or 0),
            "min_age": int(meta.get("min_age") or 0),
            "max_age": int(meta.get("max_age") or 99),
            "lat": float(meta.get("lat") or 0.0),
            "lng": float(meta.get("lng") or 0.0),
            "source": "fallback"
        })

        if len(results) >= max(limit * 3, 50):  # collect enough to sort
            break

    # nearest first
    results.sort(key=lambda x: x["distance_km"])
    return results[:limit]


# =========================
# Main API: Generate Recommendations
# =========================
async def generate_recommendations(child_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    try:
        # ensure caches are ready (startup should do this, but this is a safety net)
        if STATE.model is None or STATE.child_encoder is None or STATE.activity_encoder is None:
            load_assets_once()

        if STATE.matrix is None or not STATE.activity_meta:
            # try refresh once (non-force) then fallback
            await refresh_ai_cache(force=False)

        # cold-start cases -> fallback
        if not STATE.child_encoder or child_id not in STATE.child_encoder:
            return _fallback_recommendations(child_id, limit)

        if STATE.matrix is None:
            return _fallback_recommendations(child_id, limit)

        user_idx = STATE.child_encoder[child_id]

        # Recommend top N then enrich metadata + distance
        recs = STATE.model.recommend(
            user_idx,
            STATE.matrix[user_idx],
            N=max(50, limit * 5),
            filter_already_liked_items=False
        )

        child = STATE.child_meta.get(child_id, {})
        child_lat = float(child.get("lat") or 0.0)
        child_lng = float(child.get("lng") or 0.0)

        results: List[Dict[str, Any]] = []
        reverse_map = STATE.reverse_activity_map or {}

        for item_idx, score in recs:
            item_idx = int(item_idx)
            score = float(score)

            if item_idx not in reverse_map:
                continue

            aid = reverse_map[item_idx]
            meta = STATE.activity_meta.get(aid)
            if not meta:
                continue

            dist = calc_distance(
                child_lat, child_lng,
                float(meta.get("lat") or 0.0),
                float(meta.get("lng") or 0.0),
            )

            results.append({
                "activity_id": aid,
                "activity_name": meta.get("activity_name"),
                "score": score,
                "distance_km": round(dist, 2),
                "category": meta.get("category"),
                "price": float(meta.get("price") or 0.0),
                "duration_hours": int(meta.get("duration_hours") or 0),
                "min_age": int(meta.get("min_age") or 0),
                "max_age": int(meta.get("max_age") or 99),
                "lat": float(meta.get("lat") or 0.0),
                "lng": float(meta.get("lng") or 0.0),
                "source": "als"
            })

            if len(results) >= max(limit * 3, 50):
                break

        # sort by nearest then score (مثل منطقك بس بدون ما نقتل السيرفر)
        results.sort(key=lambda x: (x["distance_km"], -x["score"]))
        return results[:limit]

    except Exception:
        logger.exception("AI recommendation failed for child_id=%s", child_id)
        # last resort
        return _fallback_recommendations(child_id, limit)
