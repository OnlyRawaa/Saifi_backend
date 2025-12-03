from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class ProviderRegister(BaseModel):
    name: str = Field(..., min_length=2)

    # واحد فقط من الاثنين (إيميل أو هاتف)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, min_length=10, max_length=10)

    location_lat: float
    location_lng: float
    address: str = Field(..., min_length=5)
    password: str = Field(..., min_length=8)


class ProviderLogin(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str = Field(..., min_length=8)
