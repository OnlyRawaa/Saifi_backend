import pandas as pd
import pickle
from database import database
from scipy.sparse import csr_matrix
import math
import traceback
import ast

# Load model once
with open("saifi_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("child_encoder.pkl", "rb") as f:
    child_encoder = pickle.load(f)

with open("activity_encoder.pkl", "rb") as f:
    activity_encoder = pickle.load(f)

reverse_activity_map = {v: k for k, v in activity_encoder.items()}


async def load_dataset():
    children = await database.fetch_all("""
        SELECT child_id, age, gender, interests, lat as child_lat, lng as child_lng
        FROM children
    """)

    activities = await database.fetch_all("""
        SELECT activity_id, name AS activity_name, category, price, duration_hours,
               min_age, max_age, lat AS activity_lat, lng AS activity_lng
        FROM activities
    """)

    bookings = await database.fetch_all("""
        SELECT child_id, activity_id, rating
        FROM bookings
        WHERE rating IS NOT NULL
    """)

    df = pd.DataFrame(bookings)
    df = df.merge(pd.DataFrame(children), on="child_id")
    df = df.merge(pd.DataFrame(activities), on="activity_id")

    return df


def build_matrix(df):
    users = df["child_id"].map(child_encoder)
    items = df["activity_id"].map(activity_encoder)

    alpha = 40
    confidence = 1 + alpha * df["rating"]

    matrix = csr_matrix(
        (confidence, (users, items)),
        shape=(len(child_encoder), len(activity_encoder))
    )

    return matrix


def calc_distance(lat1, lon1, lat2, lon2):
    try:
        R = 6371
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)

        a = (math.sin(d_lat / 2) ** 2 +
             math.cos(math.radians(lat1)) *
             math.cos(math.radians(lat2)) *
             math.sin(d_lon / 2) ** 2)

        return 2 * R * math.asin(math.sqrt(a))
    except:
        return 9999


async def generate_recommendations(child_id: int, limit: int = 10):
    try:
        df = await load_dataset()
        if df.empty:
            return []

        matrix = build_matrix(df)
        df_unique = df.drop_duplicates(subset=["activity_id"])

        if child_id not in child_encoder:
            return []

        user_idx = child_encoder[child_id]

        recs = model.recommend(
            user_idx,
            matrix[user_idx],
            N=50,
            filter_already_liked_items=False
        )

        child = df[df["child_id"] == child_id].iloc[0]

        lat = float(child["child_lat"])
        lng = float(child["child_lng"])

        results = []

        for rec in recs:
            item_idx = int(rec[0])
            score = float(rec[1])

            if item_idx not in reverse_activity_map:
                continue

            activity_id = reverse_activity_map[item_idx]

            act = df_unique[df_unique["activity_id"] == activity_id]
            if act.empty:
                continue

            act = act.iloc[0]

            dist = calc_distance(
                lat, lng,
                float(act["activity_lat"]),
                float(act["activity_lng"])
            )

            results.append({
                "activity_id": int(activity_id),
                "activity_name": act["activity_name"],
                "score": score,
                "price": float(act["price"]),
                "category": act["category"],
                "duration_hours": int(act["duration_hours"]),
                "distance_km": round(dist, 2),
                "min_age": int(act["min_age"]),
                "max_age": int(act["max_age"]),
                "lat": float(act["activity_lat"]),
                "lng": float(act["activity_lng"])
            })

        # sort: nearest, then highest score
        results.sort(key=lambda x: (x["distance_km"], -x["score"]))

        return results[:limit]

    except Exception as e:
        print("AI ERROR:", e)
        traceback.print_exc()
        return []
