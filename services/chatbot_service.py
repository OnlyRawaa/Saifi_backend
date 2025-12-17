from google.cloud import dialogflow_v2 as dialogflow
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "saifibot.json"

PROJECT_ID = "saifibot-sxso"

def detect_intent(text: str, lang: str):
    text_lower = text.lower()

    # BOOK ACTIVITY
    # BOOK ACTIVITY
    if "book" in text_lower and "activity" in text_lower:
        return {
            "reply": (
                "Okay 😊 Here’s how to book an activity:\n"
                "• Home → Browse activities\n"
                "• Select an activity\n"
                "• Choose the suitable details\n"
                "• Confirm and submit the booking\n\n"
                "I can take you directly to the activities page 👇"
            ),
            "intent": "book_activity"
            }


    # ADD CHILD
    # ADD CHILD
    if "add" in text_lower and "child" in text_lower:
        return {
            "reply": (
                "Sure 👶 Here’s how to add a child:\n"
                "• Go to the Children section\n"
                "• Tap the (+) button in the navigation bar\n"
                "• Enter your child’s details\n"
                "• Save the information\n\n"
                "I can take you to the add child page 👇"
            ),
            "intent": "add_child"
        }


    # TRACK BOOKINGS
    # TRACK BOOKINGS
    if "track" in text_lower and "booking" in text_lower:
        return {
            "reply": (
                "No problem 📅 Here’s how to track your bookings:\n"
                "• Home → My Bookings\n"
                "• View all your current and past bookings\n\n"
                "I can open your bookings page for you 👇"
            ),
            "intent": "track_my_booking"
        }


    # KIDS INFORMATION
    # KIDS INFORMATION
    if "kids" in text_lower or "children" in text_lower:
        return {
            "reply": (
                "Here’s where you can view your kids’ information 🧒:\n"
                "• Profile → Kids Information\n"
                "• View all added children and their details\n\n"
                "I can take you there now 👇"
            ),
            "intent": "kids_information"
        }


    # ABOUT PLATFORM
    if "about" in text_lower or "platform" in text_lower:
        return {
            "reply":
            "Saifi is a smart platform that helps parents discover, compare, and manage summer activities for their children. "
            "You can find more details in Profile → About Us, where you can also view the Terms & Conditions.",
            "intent": None
        }

    # FALLBACK
    return {
        "reply": "Sorry, I didn’t quite understand that. Could you clarify?",
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
