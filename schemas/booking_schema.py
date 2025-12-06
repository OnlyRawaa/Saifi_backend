from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date, datetime
from typing import Optional, Literal


# =========================
# ✅ CREATE BOOKING (FROM FLUTTER)
# =========================
class BookingCreate(BaseModel):
    parent_id: UUID
    child_id: UUID
    activity_id: UUID

    start_date: date
    end_date: date

    notes: Optional[str] = None


# =========================
# ✅ UPDATE BOOKING STATUS (PROVIDER)
# =========================
class BookingUpdate(BaseModel):
    status: Literal["pending", "confirmed", "rejected"]


# =========================
# ✅ BOOKING RESPONSE (OUTPUT)
# =========================
class BookingOut(BaseModel):
    booking_id: UUID

    parent_id: UUID
    child_id: UUID
    activity_id: UUID

    start_date: date
    end_date: date
    notes: Optional[str]

    status: Literal["pending", "confirmed", "rejected"]

    created_at: datetime
