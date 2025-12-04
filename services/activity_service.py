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
                    capacity,
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
                data["capacity"],          # ✅ كانت سبب الخراب
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
                    capacity,
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
    # ✅ Get Activities By Provider ✅
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

    # =========================
    # ✅ Update Activity ✅
    # =========================
    @staticmethod
    def update_activity(activity_id: str, data: dict):
        conn = get_connection()
        cur = conn.cursor()

        try:
            if not data:
                return False

            fields = []
            values = []

            for key, value in data.items():
                fields.append(f"{key} = %s")
                values.append(value)

            values.append(activity_id)

            query = f"""
                UPDATE activities
                SET {", ".join(fields)}
                WHERE activity_id = %s
            """

            cur.execute(query, tuple(values))

            if cur.rowcount == 0:
                return False

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cur.close()
            conn.close()
