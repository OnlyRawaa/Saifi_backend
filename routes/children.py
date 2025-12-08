from fastapi import APIRouter, HTTPException
from services.child_service import ChildService
from schemas.child_schema import ChildCreate
from datetime import date
from services.activity_service import ActivityService

from uuid import UUID

router = APIRouter(prefix="/children", tags=["Children"])


# =========================
# ✅ Get All Children
# =========================
@router.get("/")
def get_all_children():
    try:
        children = ChildService.get_all_children()
        return {"data": children}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch children: {str(e)}"
        )


# =========================
# ✅ Update Child
# =========================
@router.put("/{child_id}")
def update_child(child_id: UUID, data: dict):
    try:
        updated = ChildService.update_child(str(child_id), data)

        if not updated:
            raise HTTPException(status_code=404, detail="Child not found")

        return {"message": "Child updated successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Update failed: {str(e)}"
        )

# =========================
# ✅ delete Child
# =========================
@router.delete("/children/{child_id}")
def delete_child(child_id: str):
    try:
        deleted = ChildService.delete_child(child_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Child not found")

        return {"message": "Child deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# =========================
# ✅ Get Children By Parent ✅ (FIXED ✅)
# =========================
@router.get("/by-parent/{parent_id}")
def get_children_by_parent(parent_id: UUID):
    try:
        children = ChildService.get_children_by_parent(str(parent_id))
        return {"data": children}   # ✅ هذا كان سبب اختفاء الأطفال
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch children: {str(e)}"
        )


# =========================
# ✅ Initial Recommendations (Cold Start)
# =========================
@router.get("/{child_id}/initial-recommendations")
def initial_recommendations(child_id: UUID):
    try:
        child = ChildService.get_child_with_parent_location(str(child_id))

        if not child:
            raise HTTPException(status_code=404, detail="Child not found")

        birth = child["birthdate"]  # هذا بالفعل date من PostgreSQL

        today = date.today()
        age = today.year - birth.year - (
            (today.month, today.day) < (birth.month, birth.day)
        )

        activities = ActivityService.get_filtered_activities_by_provider_location(
            parent_lat=child["parent_lat"],
            parent_lng=child["parent_lng"],
            age=age,
            gender=child["gender"]
        )

        return {
            "type": "cold_start",
            "child_id": str(child_id),
            "recommendations": activities
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate recommendations: {str(e)}"
        )

# =========================
# ✅ Create Child
# =========================
@router.post("/create")
@router.post("/create")
def create_child(child: ChildCreate):
    try:
        new_id = ChildService.create_child(child.dict())
        return {
            "message": "Child created successfully",
            "child_id": new_id
        }

    except Exception as e:
        # ✅ Duplicate child case
        if "already exists" in str(e):
            raise HTTPException(
                status_code=409,
                detail="Child already exists with same name, birthdate, and gender"
            )

        # ✅ Any other unexpected error
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create child: {str(e)}"
        )

