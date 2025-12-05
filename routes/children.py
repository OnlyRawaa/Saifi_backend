from fastapi import APIRouter, HTTPException
from services.child_service import ChildService
from schemas.child_schema import ChildCreate
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
# ✅ Update Child ✅ هذا اللي كان ناقص فعليًا عندك
# =========================
@router.put("/{child_id}")
def update_child(child_id: UUID, data: dict):
    try:
        updated = ChildService.update_child(str(child_id), data)

        if not updated:
            raise HTTPException(status_code=404, detail="Child not found")

        return {"message": "Child updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# ✅ Get Children By Parent
# =========================
@router.get("/by-parent/{parent_id}")
def get_children_by_parent(parent_id: UUID):
    try:
        children = ChildService.get_children_by_parent(str(parent_id))
        return children
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch children: {str(e)}"
        )


# =========================
# ✅ Create Child
# =========================
@router.post("/create")
def create_child(child: ChildCreate):
    try:
        new_id = ChildService.create_child(child.dict())
        return {
            "message": "Child created successfully",
            "child_id": new_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create child: {str(e)}"
        )
