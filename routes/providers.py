from fastapi import APIRouter, HTTPException
from services.provider_service import ProviderService
from schemas.provider_schema import ProviderRegister, ProviderLogin

router = APIRouter(prefix="/providers", tags=["Providers"])


# =========================
# ✅ REGISTER
# =========================
@router.post("/register")
def register_provider(data: ProviderRegister):
    try:
        result = ProviderService.register_provider(data.dict())

        return {
            "message": "Provider registered successfully",
            "provider_id": result["provider_id"]
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Provider registration failed: {str(e)}"
        )


# =========================
# ✅ LOGIN
# =========================
@router.post("/login")
def login_provider(data: ProviderLogin):
    try:
        provider = ProviderService.login_provider(
            data.email,
            data.password
        )

        if not provider:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        return {
            "message": "Login successful",
            "provider": provider
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Login failed: {str(e)}"
        )


# =========================
# ✅ GET ALL PROVIDERS
# =========================
@router.get("/")
def get_all_providers():
    try:
        return ProviderService.get_all_providers()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch providers: {str(e)}"
        )
