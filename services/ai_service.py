import pandas as pd
import pickle
from database import database
from scipy.sparse import csr_matrix
import math
import traceback

# ============================
# Load model & encoders once
# ============================
with open("saifi_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("child_encoder.pkl", "rb") as f:
    child_encoder = pickle.load(f)

with open("activity_encoder.pkl", "rb") as f:
    activity_encoder = pickle.load(f)

# internal ALS index → real UUID
reverse_activity_map = {v: k for k, v in activity_encoder.items()}


# ============================
# Load dataset from PostgreSQL
# ============================
async def load_dataset():
    children = await database.fetch_all("""
        SELECT child_id, age, gender, interests, lat AS child_lat, lng AS child_lng
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

    if not bookings:
        return pd.DataFrame()

    df = pd.DataFrame(bookings)
    df = df.merge(pd.DataFrame(children), on="child_id", how="left")
    df = df.merge(pd.DataFrame(activities), on="activity_id", how="left")

    return df


# ============================
# Build sparse matrix
# ============================
def build_matrix(df: pd.DataFrame):
    users = df["child_id"].map(child_encoder)
    items = df["activity_id"].map(activity_encoder)

    alpha = 40
    confidence = 1 + alpha * df["rating"].astype(float)

    return csr_matrix(
        (confidence, (users, items)),
        shape=(len(child_encoder), len(activity_encoder))
    )


# ============================
# Distance helper
# ============================
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
        return 9999  # fallback if data missing


# ============================
# Generate Recommendations
# ============================
async def generate_recommendations(child_id: str, limit: int = 10):
    try:
        df = await load_dataset()

        if df.empty:
            print("⚠️ No dataset loaded from DB.")
            return []

        # remove activities without location
        df = df.dropna(subset=["activity_lat", "activity_lng"])

        # Keep unique activities for metadata
        df_unique = df.drop_duplicates(subset=["activity_id"])

        # UUID check here
        if child_id not in child_encoder:
            print("⚠️ Child not found in encoder:", child_id)
            return []

        # ALS user index
        user_idx = child_encoder[child_id]

        # FULL matrix
        matrix = build_matrix(df)

        # Predict scores
        recs = model.recommend(
            user_idx,
            matrix[user_idx],
            N=50,
            filter_already_liked_items=False
        )

        # Child metadata row
        child_row = df[df["child_id"] == child_id].iloc[0]

        child_lat = float(child_row.get("child_lat", 0))
        child_lng = float(child_row.get("child_lng", 0))

        results = []

        for rec in recs:
            item_idx = int(rec[0])    # ALS internal index
            score = float(rec[1])

            if item_idx not in reverse_activity_map:
                continue

            real_activity_id = reverse_activity_map[item_idx]

            # Fetch activity metadata
            act = df_unique[df_unique["activity_id"] == real_activity_id]

            if act.empty:
                continue

            act = act.iloc[0]

            dist = calc_distance(
                child_lat,
                child_lng,
                float(act["activity_lat"]),
                float(act["activity_lng"])
            )

            results.append({
                "activity_id": real_activity_id,                          # UUID STR هنا
                "activity_name": act["activity_name"],
                "score": score,
                "distance_km": round(dist, 2),
                "category": act["category"],
                "price": float(act["price"]),
                "duration_hours": int(act["duration_hours"]),
                "min_age": int(act["min_age"]),
                "max_age": int(act["max_age"]),
                "lat": float(act["activity_lat"]),
                "lng": float(act["activity_lng"])
            })

        # Sort by: nearest → highest score
        results.sort(key=lambda x: (x["distance_km"], -x["score"]))

        return results[:limit]

    except Exception as e:
        print("❌ AI ERROR:", e)
        traceback.print_exc()
        return []
