class Booking:
    def __init__(
        self,
        booking_id,
        parent_id,
        child_id,
        activity_id,
        provider_id,
        status,
        booking_date,
        created_at
    ):
        self.booking_id = booking_id
        self.parent_id = parent_id
        self.child_id = child_id
        self.activity_id = activity_id
        self.provider_id = provider_id
        self.status = status
        self.booking_date = booking_date
        self.created_at = created_at

    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "parent_id": self.parent_id,
            "child_id": self.child_id,
            "activity_id": self.activity_id,
            "provider_id": self.provider_id,
            "status": self.status,
            "booking_date": self.booking_date,
            "created_at": self.created_at
        }
