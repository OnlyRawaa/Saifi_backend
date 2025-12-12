from fastapi import APIRouter
from services.ai_service import generate_recommendations
from services.ai_cache import MODEL, MATRIX

router = APIRouter(prefix="/ai", tags=["AI"])


@router.get("/recommend")
async def recommend(child_id: str, limit: int = 10):
    data = await generate_recommendations(child_id, limit)
    return {
        "child_id": child_id,
        "recommendations": data
    }


@router.get("/health")
def ai_health():
    return {
        "model_loaded": MODEL is not None,
        "matrix_loaded": MATRIX is not None
    }
