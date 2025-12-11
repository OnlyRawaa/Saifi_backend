import pickle
from db.connection import get_db_connection


class AIService:

    # ======================================
    # Load the AI recommendation model
    # ======================================
    @staticmethod
    def load_model():
        try:
            with open("models/recommender.pkl", "rb") as f:
                model = pickle.load(f)
            return model
        except Exception as e:
            raise Exception(f"Failed to load AI model: {str(e)}")

    # ======================================
    # Fetch children linked to a parent
    # ======================================
    @staticmethod
    def get_children(parent_id: str):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT child_id, age, gender
            FROM children
            WHERE parent_id = %s
            """,
            (parent_id,)
        )

        rows = cur.fetchall()
        cur.close()
        conn.close()

        return [
            {
                "child_id": r[0],
                "age": r[1],
                "gender": r[2]
            }
            for r in rows
        ]

    # ======================================
    # Fetch all available activities
    # ======================================
    @staticmethod
    def get_all_activities():
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT activity_id, title, category, age_from, age_to, gender, provider_id
            FROM activities
            """
        )

        rows = cur.fetchall()
        cur.close()
        conn.close()

        return [
            {
                "activity_id": r[0],
                "title": r[1],
                "category": r[2],
                "age_from": r[3],
                "age_to": r[4],
                "gender": r[5],
                "provider_id": r[6],
            }
            for r in rows
        ]

    # ======================================
    # Generate recommendations for one child
    # (The trained model handles scoring logic)
    # ======================================
    @staticmethod
    def recommend_for_child(model, child, activities):
        try:
            # Model must implement a method named "recommend"
            recommendations = model.recommend(child, activities)
            return recommendations
        except Exception as e:
            raise Exception(f"AI recommendation error: {str(e)}")

    # ======================================
    # Main function: Generate recommendations
    # for all children belonging to a parent
    # ======================================
    @staticmethod
    def get_recommendations(parent_id: str):

        # 1. Load the trained model
        model = AIService.load_model()

        # 2. Fetch parent's children
        children = AIService.get_children(parent_id)

        if not children:
            return []

        # 3. Fetch activities from DB
        activities = AIService.get_all_activities()

        results = []

        # 4. Run recommendations for each child
        for child in children:
            child_recs = AIService.recommend_for_child(model, child, activities)
            results.extend(child_recs)

        # 5. Remove duplicates using activity_id as key
        unique = {item["activity_id"]: item for item in results}.values()
        return list(unique)
