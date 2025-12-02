from fastapi import APIRouter, HTTPException
from services.auth_service import AuthService
from schemas.parent_schema import ParentCreate, ParentUpdate
from uuid import UUID

router = APIRouter(prefix="/parents", tags=["Parents"])

# =========================
# ✅ Register Parent
# =========================
@router.post("/register")
def register_parent(parent: ParentCreate):
    try:
        parent_id = AuthService.save_parent(
            first_name=parent.first_name.strip(),
            last_name=parent.last_name.strip(),
            email=parent.email.strip() if parent.email else None,
            phone=parent.phone.strip() if parent.phone else None,
            raw_password=parent.password
        )

        return {
            "message": "Parent created successfully",
            "parent_id": parent_id
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )

# =========================
# ✅ Get All Parents (NEW ✅)
# =========================
@router.get("/")
def get_all_parents():
    try:
        parents = AuthService.get_all_parents()
        return {"data": parents}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch parents: {str(e)}"
        )

# =========================
# ✅ Update Parent Profile
# =========================
@router.put("/{parent_id}")
def update_parent(parent_id: UUID, parent: ParentUpdate):
    try:
        updated = AuthService.update_parent(
            parent_id=str(parent_id),
            data=parent.dict(exclude_none=True)
        )

        if not updated:
            raise HTTPException(status_code=404, detail="Parent not found")

        return {"message": "Parent updated successfully"}

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Update failed: {str(e)}"
        )
from schemas.parent_schema import ParentLocationUpdate

# =========================
# ✅ Update Parent Location
# =========================
@router.put("/update-location")
def update_parent_location(data: ParentLocationUpdate):
    try:
        updated = AuthService.update_parent_location(
            parent_id=data.parent_id,
            lat=data.location_lat,
            lng=data.location_lng
        )

        if not updated:
            raise HTTPException(status_code=404, detail="Parent not found")

        return {"message": "Location updated successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update location: {str(e)}"
        )
