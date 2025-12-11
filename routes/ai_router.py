from fastapi import APIRouter, HTTPException
from services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["AI"])

@router.get("/recommend/{parent_id}")
def get_recommendations(parent_id: str):
    try:
        recs = AIService.get_recommendations(parent_id)
        return {"recommendations": recs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
