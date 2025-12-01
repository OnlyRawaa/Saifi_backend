from pydantic import BaseModel
from datetime import date


class BookingCreate(BaseModel):
    parent_id: str
    child_id: str
    activity_id: str
    booking_date: date


class BookingUpdate(BaseModel):
    status: str

