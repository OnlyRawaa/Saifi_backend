from pydantic import BaseModel, EmailStr, Field, root_validator
from typing import Optional


# =========================
# ✅ REGISTER SCHEMA
# =========================
class ProviderRegister(BaseModel):
    name: str = Field(..., min_length=2)

    # واحد فقط من الاثنين (إيميل أو هاتف)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, min_length=10, max_length=10)

    location_lat: float
    location_lng: float
    address: str = Field(..., min_length=5)

    password: str = Field(..., min_length=8)

    # ✅ ضمان أن واحد فقط من (email أو phone) موجود
    @root_validator
    def check_email_or_phone(cls, values):
        email = values.get("email")
        phone = values.get("phone")

        if not email and not phone:
            raise ValueError("Either email or phone must be provided")

        if email and phone:
            raise ValueError("Provide only one of email or phone, not both")

        return values


# =========================
# ✅ LOGIN SCHEMA
# =========================
class ProviderLogin(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str = Field(..., min_length=8)

    # ✅ نفس القاعدة في تسجيل الدخول
    @root_validator
    def check_login_identifier(cls, values):
        email = values.get("email")
        phone = values.get("phone")

        if not email and not phone:
            raise ValueError("Either email or phone must be provided")

        if email and phone:
            raise ValueError("Provide only one of email or phone, not both")

        return values
