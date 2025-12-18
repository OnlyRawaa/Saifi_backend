

def normalize(text: str) -> str:
    return text.lower().strip()


def contains_any(text: str, keywords: list[str]) -> bool:
    return any(word in text for word in keywords)


def detect_intent(text: str, lang: str):
    text_lower = normalize(text)

    # =========================
    # BOOK ACTIVITY
    # =========================
    if contains_any(text_lower, ["book", "booking", "reserve", "reservation"]) and \
       contains_any(text_lower, ["activity", "activities", "program", "class"]):
        return {
            "reply": (
                "Okay 😊 Here’s how to book an activity:\n"
                "• Home → Browse activities\n"
                "• Select an activity\n"
                "• Choose the suitable details\n"
                "• Confirm and submit the booking\n\n"
                "Tap the button below to go directly 👇"
            ),
            "intent": "book_activity"
        }

    # =========================
    # ADD CHILD
    # =========================
    if contains_any(text_lower, ["add", "create", "new", "add"]): and \
        contains_any(text_lower, ["child", "kid", "son", "children"]):
        return {
            "reply": (
                "Sure 👶 Here’s how to add a child:\n"
                "• Go to the Children section\n"
                "• Tap the (+) button\n"
                "• Enter your child’s details\n"
                "• Save the information\n\n"
                "Tap below to add a child 👇"
            ),
            "intent": "add_child"
        }

    # =========================
    # TRACK BOOKINGS
    # =========================
    if contains_any(text_lower, ["booking", "bookings", "my bookings", "reservations"]):
        return {
            "reply": (
                "Here’s how you can track your bookings 📅:\n"
                "• Go to the Home page\n"
                "• Open My Bookings\n"
                "• View all your current and past reservations\n\n"
                "Tap the button below to view them 👇"
            ),
            "intent": "track_my_booking"
        }

    # =========================
    # KIDS INFORMATION
    # =========================
    if contains_any(text_lower, ["kids info", "kids information", "my kids", "children info"]):
        return {
            "reply": (
                "You can view your kids’ information by:\n"
                "• Opening the Profile page\n"
                "• Selecting Kids Information\n"
                "• Viewing all added children and their details 🧒\n\n"
                "Tap below to see their profiles 👇"
            ),
            "intent": "kids_information"
        }

    # =========================
    # ABOUT PLATFORM
    # =========================
    if contains_any(text_lower, ["about", "platform", "saifi", "terms", "conditions"]):
        return {
            "reply": (
                "Saifi helps parents discover and manage summer activities for their children.\n"
                "You can learn more from Profile → About Us."
            ),
            "intent": None
        }

    # =========================
    # SMART FALLBACK (آخر حل)
    # =========================
    return {
        "reply": (
            "I can help you with:\n"
            "• Booking activities\n"
            "• Adding children\n"
            "• Tracking bookings\n"
            "• Viewing kids information\n\n"
            "Try asking me using simple words 😊"
        ),
        "intent": None
    }




    
