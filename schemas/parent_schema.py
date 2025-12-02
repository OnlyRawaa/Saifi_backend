from pydantic import BaseModel, EmailStr
from typing import Optional


class ParentLocationUpdate(BaseModel):
    parent_id: str
    location_lat: float
    location_lng: float


class ParentBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class ParentCreate(ParentBase):
    password: str


class ParentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
