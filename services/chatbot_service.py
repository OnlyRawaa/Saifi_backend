from google.cloud import dialogflow_v2 as dialogflow
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "saifibot.json"

PROJECT_ID = "saifibot-sxso"

def detect_intent(text: str, lang: str):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(PROJECT_ID, "user-session")

    text_input = dialogflow.TextInput(
        text=text,
        language_code=lang
    )

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    intent = response.query_result.intent.display_name
    reply = response.query_result.fulfillment_text

    return {
        "reply": reply,
        "intent": intent
    }
