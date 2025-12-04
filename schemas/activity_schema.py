from pydantic import BaseModel
from typing import Optional
from datetime import date


# =========================
# ✅ Base Activity Schema
# =========================
class ActivityBase(BaseModel):
    provider_id: str

    title: str
    description: Optional[str] = None

    gender: str               # male / female / both
    age_from: int
    age_to: int

    price: float
    capacity: int
    duration: int             # عدد الساعات

    type: str                 # Sports / Technology / etc
    status: bool              # Active = True / Inactive = False

    start_date: Optional[date] = None
    end_date: Optional[date] = None


# =========================
# ✅ Create Activity
# =========================
class ActivityCreate(ActivityBase):
    pass


# =========================
# ✅ Update Activity
# =========================
class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    gender: Optional[str] = None
    age_from: Optional[int] = None
    age_to: Optional[int] = None

    price: Optional[float] = None
    capacity: Optional[int] = None
    duration: Optional[int] = None

    type: Optional[str] = None
    status: Optional[bool] = None

    start_date: Optional[date] = None
    end_date: Optional[date] = None
