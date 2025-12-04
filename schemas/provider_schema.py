from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional


# =========================
# ✅ REGISTER SCHEMA
# =========================
class ProviderRegister(BaseModel):
    name: str = Field(..., min_length=2)

    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, min_length=10, max_length=10)

    location_lat: float
    location_lng: float
    address: str = Field(..., min_length=5)

    password: str = Field(..., min_length=8)

    # ✅ Pydantic v2 validator
    @model_validator(mode="after")
    def check_email_or_phone(self):
        if not self.email and not self.phone:
            raise ValueError("Either email or phone must be provided")
        if self.email and self.phone:
            raise ValueError("Provide only one of email or phone, not both")
        return self


# =========================
# ✅ LOGIN SCHEMA
# =========================
class ProviderLogin(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str = Field(..., min_length=8)

    @model_validator(mode="after")
    def check_login_identifier(self):
        if not self.email and not self.phone:
            raise ValueError("Either email or phone must be provided")
        if self.email and self.phone:
            raise ValueError("Provide only one of email or phone, not both")
        return self
class ProviderUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    address: Optional[str] = None
