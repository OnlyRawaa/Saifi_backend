from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


# =========================
# ✅ Base Activity Schema
# =========================
class ActivityBase(BaseModel):
    provider_id: str

    title: str = Field(..., min_length=2)
    description: Optional[str] = None

    gender: str = Field(..., description="male / female / both")
    age_from: int = Field(..., ge=0)
    age_to: int = Field(..., ge=0)

    price: float = Field(..., ge=0)
    capacity: int = Field(..., ge=1)
    duration: int = Field(..., ge=1)   # عدد الساعات

    type: str                          # Sports / Technology / etc
    status: bool = True                # ✅ افتراضي Active

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
