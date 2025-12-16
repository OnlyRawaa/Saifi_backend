from pydantic import BaseModel
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
    provider_id: UUID

    status: Literal["pending", "approved", "rejected"] = "pending"

    start_date: Optional[date] = None
    end_date: Optional[date] = None
    notes: Optional[str] = None


# =========================
# ✅ UPDATE BOOKING STATUS (PROVIDER)
# =========================
class BookingUpdate(BaseModel):
    status: Literal["pending", "approved", "rejected"]


# =========================
# ✅ BOOKING RESPONSE (OUTPUT)
# =========================
class BookingOut(BaseModel):
    booking_id: UUID

    parent_id: UUID
    child_id: UUID
    activity_id: UUID
    provider_id: UUID

    status: Literal["pending", "approved", "rejected"]

    start_date: Optional[date]
    end_date: Optional[date]
    notes: Optional[str]

    created_at: datetime

