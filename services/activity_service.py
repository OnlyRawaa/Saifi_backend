from db.connection import get_connection
from psycopg2.extras import RealDictCursor


class ActivityService:

    # =========================
    # ✅ Create Activity
    # =========================
    @staticmethod
    def create_activity(data: dict):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO activities (
                provider_id,
                title,
                description,
                price,
                gender,
                age_from,
                age_to,
                start_date,
                end_date
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING activity_id;
        """, (
            data["provider_id"],
            data["title"],
            data["description"],
            data["price"],
            data["gender"],
            data["age_from"],
            data["age_to"],
            data["start_date"],
            data["end_date"]
        ))

        activity_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return activity_id


    # =========================
    # ✅ Get All Active Activities
    # =========================
    @staticmethod
    def get_all_activities():
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            SELECT
                activity_id,
                provider_id,
                title,
                description,
                gender,
                age_from,
                age_to,
                price,
                duration,
                type,
                status,
                start_date,
                end_date,
                created_at
            FROM activities
            WHERE status = true;
        """)

        activities = cur.fetchall()

        cur.close()
        conn.close()

        return activities


    # =========================
    # ✅ Get Activity By ID
    # =========================
    @staticmethod
    def get_activity_by_id(activity_id: str):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(
            "SELECT * FROM activities WHERE activity_id = %s;",
            (str(activity_id),)
        )

        activity = cur.fetchone()

        cur.close()
        conn.close()

        return activity
