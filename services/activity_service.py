from db.connection import get_connection
from psycopg2.extras import RealDictCursor


class ActivityService:

    # =========================
    # ✅ Create Activity (FIXED ✅)
    # =========================
@staticmethod
def create_activity(data: dict):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO activities (
                provider_id,
                title,
                description,
                price,
                gender,
                age_from,
                age_to,
                capacity,       -- ✅ مضافة
                duration,
                type,
                status,
                start_date,
                end_date
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING activity_id;
        """, (
            data["provider_id"],
            data["title"],
            data.get("description"),
            data["price"],
            data["gender"],
            data["age_from"],
            data["age_to"],
            data["capacity"],           # ✅ كانت سبب الخراب
            data["duration"],
            data["type"],
            data.get("status", True),
            data.get("start_date"),
            data.get("end_date")
        ))

        activity_id = cur.fetchone()[0]
        conn.commit()
        return activity_id

    finally:
        cur.close()
        conn.close()

    # =========================
    # ✅ Get All Active Activities
    # =========================
    @staticmethod
    def get_all_activities():
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        try:
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

            return cur.fetchall()

        finally:
            cur.close()
            conn.close()

    # =========================
    # ✅ Get Activity By ID
    # =========================
    @staticmethod
    def get_activity_by_id(activity_id: str):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute(
                "SELECT * FROM activities WHERE activity_id = %s;",
                (activity_id,)
            )

            return cur.fetchone()

        finally:
            cur.close()
            conn.close()

    # =========================
    # ✅ Get Activities By Provider ✅ الصحيح لواجهة البروفايدر
    # =========================
    @staticmethod
    def get_activities_by_provider(provider_id: str):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute("""
                SELECT *
                FROM activities
                WHERE provider_id = %s
                ORDER BY created_at DESC;
            """, (provider_id,))

            return cur.fetchall()

        finally:
            cur.close()
            conn.close()
