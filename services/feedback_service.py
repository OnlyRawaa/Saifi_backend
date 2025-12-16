from db.connection import get_connection
from uuid import uuid4
from datetime import datetime


class FeedbackService:

    @staticmethod
    def create_feedback(data: dict):
        conn = get_connection()
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
            """,
            (
                feedback_id,
                str(data["parent_id"]),
                str(data["child_id"]),
                str(data["provider_id"]),
                str(data["activity_id"]),
                data["rating"],
                data.get("comment"),
                datetime.utcnow(),
            )
        )

        conn.commit()
        cursor.close()
        conn.close()

        return feedback_id
