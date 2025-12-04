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
        address=None,          # ✅ أضفنا العنوان هنا
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
        self.address = address        # ✅ حفظ العنوان
        self.description = description
        self.password_hash = password_hash
        self.created_at = created_at


# ========== INPUT MODEL ==========
class ProviderCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None   # ✅ عشان يقبل phone-only
    phone: Optional[str] = None
    description: Optional[str]
    password: str
    location_lat: Optional[float]     # ✅ مطابقة لما يرسله Flutter
    location_lng: Optional[float]
    address: Optional[str]            # ✅ الآن Flutter لن يكسر النظام

    class Config:
        orm_mode = True


# ========== RESPONSE MODEL ==========
class ProviderResponse(BaseModel):
    provider_id: str                  # ✅ UUID وليس int
    name: str
    email: Optional[EmailStr]
    phone: Optional[str]
    description: Optional[str]
    location_lat: Optional[float]
    location_lng: Optional[float]
    address: Optional[str]            # ✅ للعرض في الواجهة إن لزم

    class Config:
        orm_mode = True
# ========== ProviderUpdate ==========
class ProviderUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    address: Optional[str] = None
