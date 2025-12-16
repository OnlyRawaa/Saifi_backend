from google.cloud import dialogflow_v2 as dialogflow
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "saifibot.json"

PROJECT_ID = "saifibot-sxso"

def detect_intent(text: str, lang: str):
    text_lower = text.lower()

    # 1️⃣ Booking intent (priority)
    if "book" in text_lower:
        return {
            "reply": "Great! Let’s book an activity. I’ll guide you step by step.",
            "intent": "book_activity"
        }

    # 2️⃣ Activities / programs
    if any(word in text_lower for word in ["activity", "activities", "program", "programs"]):
        return {
            "reply": "Sure! I can help you with activities 😊 Would you like to browse activities or book one?",
            "intent": "browse_activities"
        }

    # 3️⃣ Add child
    if "add" in text_lower and "child" in text_lower:
