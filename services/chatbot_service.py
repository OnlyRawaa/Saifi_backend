from google.cloud import dialogflow_v2 as dialogflow
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "saifibot.json"

PROJECT_ID = "saifibot-sxso"

def detect_intent(text: str, lang: str):
    text_lower = text.lower()
    
    if "manage" in text_lower and "booking" in text_lower:
        return {
            "reply": "Sure! Redirecting you to your bookings.",
            "intent": "manage_booking"
        }

    # 1️⃣ Book activity
    if "book" in text_lower:
        return {
            "reply": "Great! Let’s book an activity. I’ll guide you step by step.",
            "intent": "book_activity"
        }

    # 2️⃣ Browse activities
    if any(word in text_lower for word in ["activity", "activities", "program", "programs"]):
        return {
            "reply": "Sure! I can help you with activities 😊 Would you like to browse activities or book one?",
            "intent": "browse_activities"
        }

    # 3️⃣ Add child
    if "add" in text_lower and "child" in text_lower:
        return {
            "reply": "No problem! Let’s add a child to your profile.",
            "intent": "add_child"
        }
    if "about" in text_lower or "platform" in text_lower:
        return {
            "reply": "Saifi is a smart platform that helps parents discover, compare, and manage summer activities for their children. "
                 "You can find more details in Profile → About Us, where you can also view the Terms & Conditions.",
            "intent": None
    }



    # 4️⃣ Dialogflow fallback
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(PROJECT_ID, "user-session")

    text_input = dialogflow.TextInput(
        text=text,
        language_code=lang
    )

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={
            "session": session,
            "query_input": query_input
        }
    )

    intent = response.query_result.intent.display_name
    reply = response.query_result.fulfillment_text

    if not reply:
        reply = "Sorry, I didn’t quite understand that. Could you clarify?"
        intent = None

    return {
        "reply": reply,
        "intent": intent
    }
