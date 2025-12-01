from pydantic import BaseModel, EmailStr
from typing import Optional


# ====== DB Model (Internal Use) ======
class Parent:
    def __init__(
        self,
        parent_id=None,
        first_name=None,
        last_name=None,
        email=None,
        phone=None,
        password_hash=None,
        location_lat=None,
        location_lng=None,
        children_count=0,
        created_at=None
    ):
        self.parent_id = parent_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password_hash = password_hash
        self.location_lat = location_lat
        self.location_lng = location_lng
        self.children_count = children_count
        self.created_at = created_at


# ====== API INPUT MODEL ======
class ParentCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: str


# ====== API RESPONSE MODEL ======
class ParentResponse(BaseModel):
    parent_id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    children_count: int
    location_lat: Optional[float]
    location_lng: Optional[float]

    class Config:
        orm_mode = True
