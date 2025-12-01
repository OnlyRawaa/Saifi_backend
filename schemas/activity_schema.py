from pydantic import BaseModel
from typing import Optional
from datetime import date


class ActivityBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    capacity: int
    start_date: date
    end_date: date
    provider_id: str


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    capacity: Optional[int] = None

