import uuid
from db.connection import get_connection
from psycopg2.extras import RealDictCursor


class ChildService:

    # =========================
    # ✅ Get All Children
    # =========================
    @staticmethod
    def get_all_children():
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            SELECT *
            FROM children
            ORDER BY created_at DESC
        """)

        rows = cur.fetchall()
        cur.close()
        conn.close()

        return rows


    # =========================
    # ✅ Get Children By Parent
    # =========================
    @staticmethod
    def get_children_by_parent(parent_id: str):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            SELECT 
                child_id,
                parent_id,
                first_name,
                last_name,
                birthdate,
                gender,
                interests,
                notes,
                created_at
            FROM children
            WHERE parent_id = %s
            ORDER BY created_at DESC
        """, (parent_id,))

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return rows


    # =========================
    # ✅ Create Child (WITH DUPLICATE CHECK)
    # =========================
    @staticmethod
    def create_child(data: dict):
        conn = get_connection()
        cur = conn.cursor()

        child_id = str(uuid.uuid4())
        interests = data.get("interests") or []
        notes = data.get("notes")

        try:
            # ✅ 1. Check if child already exists
            cur.execute("""
                SELECT 1
                FROM children
                WHERE 
                    parent_id = %s
                AND first_name = %s
                AND last_name = %s
                AND birthdate = %s
                AND gender = %s
            """, (
                data["parent_id"],
                data["first_name"],
                data["last_name"],
                data["birthdate"],
                data["gender"]
            ))

            if cur.fetchone():
                raise Exception("Child already exists with same name, birthdate, and gender")

            # ✅ 2. Insert if not duplicate
            cur.execute("""
                INSERT INTO children (
                    child_id,
                    parent_id,
                    first_name,
                    last_name,
                    birthdate,
                    gender,
                    interests,
                    notes
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                child_id,
                data["parent_id"],
                data["first_name"],
                data["last_name"],
                data["birthdate"],
                data["gender"],
                interests,
                notes
            ))

            conn.commit()
            return child_id

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cur.close()
            conn.close()

    # =========================
    # ✅ Get Child With Parent Location (For AI Cold Start)
    # =========================

    @staticmethod
    def get_child_with_parent_location(child_id: str):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute("""
                SELECT 
                    c.child_id,
                    c.birthdate,
                    c.gender,
                    p.location_lat AS parent_lat,
                    p.location_lng AS parent_lng
                FROM children c
                JOIN parents p ON c.parent_id = p.parent_id
                WHERE c.child_id = %s;
            """, (child_id,))

            return cur.fetchone()

        finally:
            cur.close()
            conn.close()


    # =========================
    # ✅ Update Child (FIXED & SAFE)
    # =========================
    @staticmethod
    def update_child(child_id: str, data: dict):
        if not data:
            return False  # ✅ يمنع تنفيذ UPDATE فاضي

        conn = get_connection()
        cur = conn.cursor()

        fields = []
        values = []

        for key, value in data.items():
            fields.append(f"{key} = %s")
            values.append(value)

        values.append(child_id)

        try:
            cur.execute(f"""
                UPDATE children
                SET {', '.join(fields)}
                WHERE child_id = %s
            """, tuple(values))

            updated = cur.rowcount > 0
            conn.commit()

            return updated

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cur.close()
            conn.close()
