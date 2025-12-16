from fastapi import APIRouter
from pydantic import BaseModel
from services.chatbot_service import detect_intent

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

class ChatRequest(BaseModel):
    text: str
    lang: str = "ar"

@router.post("/message")
def chatbot_message(data: ChatRequest):
    return detect_intent(data.text, data.lang)
