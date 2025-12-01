from pydantic import BaseModel, EmailStr
from typing import Optional


# ========== INTERNAL DB MODEL ==========
class Provider:
    def __init__(
        self,
        provider_id=None,
        name=None,
        email=None,
        phone=None,
        location_lat=None,
        location_lng=None,
        description=None,
        password_hash=None,
        created_at=None
    ):
        self.provider_id = provider_id
        self.name = name
        self.email = email
        self.phone = phone
        self.location_lat = location_lat
        self.location_lng = location_lng
        self.description = description
        self.password_hash = password_hash
        self.created_at = created_at



# ========== INPUT MODEL ==========
class ProviderCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    description: Optional[str]
    password: str



# ========== RESPONSE MODEL ==========
class ProviderResponse(BaseModel):
    provider_id: int
    name: str
    email: EmailStr
    phone: str
    description: Optional[str]
    location_lat: Optional[float]
    location_lng: Optional[float]

    class Config:
        orm_mode = True
