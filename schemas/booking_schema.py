from pydantic import BaseModel
from uuid import UUID
from datetime import date


class BookingCreate(BaseModel):
    parent_id: UUID
    child_id: UUID
    activity_id: UUID
    provider_id: UUID   # ✅ كان مفقود وهو سبب الانهيار
    status: str         # ✅ كان مفقود أيضًا
    booking_date: date


class BookingUpdate(BaseModel):
    booking_id: UUID
    status: str
