from fastapi import APIRouter, HTTPException
from services.provider_service import ProviderService

from schemas.provider_schema import ProviderRegister, ProviderLogin, ProviderUpdate

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
            "provider_id": str(result["provider_id"])
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Provider registration failed: {str(e)}"
        )
# =========================
# ✅ get_activity_by_id
# =========================
@router.get("/{activity_id}")
def get_activity_by_id(activity_id: str):
    try:
        activity = ActivityService.get_activity_by_id(activity_id)

        if not activity:
            raise HTTPException(
                status_code=404,
                detail="Activity not found"
            )

        return activity   # ⛔ لا ترجعيه داخل data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch activity: {str(e)}"
        )

# =========================
# ✅ LOGIN (EMAIL OR PHONE)
# =========================
@router.post("/login")
def login_provider(data: ProviderLogin):
    try:
        provider = ProviderService.login_provider(
            email=data.email,
            phone=data.phone,
            password=data.password
        )

        if not provider:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        return {
            "message": "Login successful",
            "provider_id": str(provider["provider_id"]),
            "name": provider["name"],
            "email": provider.get("email"),
            "phone": provider.get("phone"),
            "location_lat": provider.get("location_lat"),
            "location_lng": provider.get("location_lng"),
            "address": provider.get("address"),
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


# =========================
# ✅ GET PROVIDER BY ID (هذا الذي ينقصك)
# =========================
@router.get("/{provider_id}")
def get_provider_by_id(provider_id: str):
    try:
        provider = ProviderService.get_provider_by_id(provider_id)

        if not provider:
            raise HTTPException(
                status_code=404,
                detail="Provider not found"
            )

        return provider

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch provider: {str(e)}"
        )
# =========================
# ✅ UPDATE PROVIDER
# =========================
@router.put("/{provider_id}")
def update_provider(provider_id: str, data: ProviderUpdate):
    try:
        ProviderService.update_provider(
            provider_id,
            data.dict(exclude_unset=True)
        )

        return {
            "message": "Provider updated successfully"
        }

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Provider not found"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update provider: {str(e)}"
        )

