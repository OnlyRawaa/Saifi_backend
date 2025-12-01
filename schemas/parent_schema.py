from pydantic import BaseModel, EmailStr
from typing import Optional


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
