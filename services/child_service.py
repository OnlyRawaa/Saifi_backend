from psycopg2.extras import RealDictCursor
from db.connection import get_connection


class ChildService:

    @staticmethod
    def get_all_children():
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM children;")
        children = cur.fetchall()

        cur.close()
        conn.close()
        return children

    @staticmethod
    def create_child(data: dict):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        query = """
            INSERT INTO children (
                first_name,
                last_name,
                birthdate,
                gender,
                parent_id,
                interests
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING child_id;
        """

        cur.execute(query, (
            data["first_name"],
            data["last_name"],
            data["birthdate"],
            data["gender"],
            data["parent_id"],
            data["interests"],
        ))

        new_id = cur.fetchone()["child_id"]
        conn.commit()

        cur.close()
        conn.close()
        return new_id
