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
    # ✅ Get Children By Parent ID  <<< هذا كان ناقصك
    # =========================
    @staticmethod
    def get_children_by_parent(parent_id: str):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            SELECT *
            FROM children
            WHERE parent_id = %s
            ORDER BY created_at DESC
        """, (parent_id,))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        return rows


@staticmethod
def create_child(data: dict):
    conn = get_connection()
    cur = conn.cursor()

    child_id = str(uuid.uuid4())

    interests = data.get("interests", [])

    try:
        cur.execute("""
            INSERT INTO children (
                child_id,
                parent_id,
                first_name,
                last_name,
                birthdate,
                gender,
                interests
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            child_id,
            data["parent_id"],
            data["first_name"],
            data["last_name"],
            data["birthdate"],
            data["gender"],
            interests
        ))

        conn.commit()
        return child_id

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cur.close()
        conn.close()

