from db.database import get_db_connection
from uuid import uuid4
from datetime import datetime


class FeedbackService:

    @staticmethod
    def create_feedback(data: dict):
        conn = get_db_connection()
        cursor = conn.cursor()

        feedback_id = str(uuid4())

        cursor.execute(
            """
            INSERT INTO feedback (
                feedback_id,
                parent_id,
                child_id,
                provider_id,
                activity_id,
                rating,
                comment,
                date
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING feedback_id;
            """,
            (
                feedback_id,
                data["parent_id"],
                data["child_id"],
                data["provider_id"],
                data["activity_id"],
                data["rating"],
                data.get("comment"),
                datetime.utcnow()
            )
        )

        conn.commit()
        cursor.close()
        conn.close()

        return feedback_id
