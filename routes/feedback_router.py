from fastapi import APIRouter, HTTPException
from schemas.feedback_schema import FeedbackCreate
from services.feedback_service import FeedbackService

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("")
def create_feedback(data: FeedbackCreate):
    try:
        feedback_id = FeedbackService.create_feedback(data.dict())
        return {
            "message": "Feedback submitted successfully",
            "feedback_id": feedback_id
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Create feedback failed: {str(e)}"
        )
