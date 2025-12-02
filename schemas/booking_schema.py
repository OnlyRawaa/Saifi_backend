from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date
from typing import Literal


# =========================
# ✅ CREATE BOOKING
# =========================
class BookingCreate(BaseModel):
    parent_id: UUID
    child_id: UUID
    activity_id: UUID
    provider_id: UUID

    status: Literal["pending", "confirmed", "rejected"] = "pending"
    booking_date: date = Field(..., example="2025-12-02")


# =========================
# ✅ UPDATE BOOKING STATUS
# =========================
class BookingUpdate(BaseModel):
    booking_id: UUID
    status: Literal["pending", "confirmed", "rejected"]
