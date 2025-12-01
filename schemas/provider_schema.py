from pydantic import BaseModel, EmailStr, Field


class ProviderRegister(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=10)
    location_lat: float
    location_lng: float
    description: str
    password: str = Field(..., min_length=8)


class ProviderLogin(BaseModel):
    email: EmailStr
    password: str
