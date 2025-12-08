from fastapi import APIRouter, HTTPException
from services.activity_service import ActivityService
from schemas.activity_schema import ActivityCreate, ActivityUpdate
from uuid import UUID

router = APIRouter(prefix="/activities", tags=["Activities"])


# =========================
# ✅ Create Activity
# =========================
@router.post("/create")
def add_activity(data: ActivityCreate):
    try:
        activity_id = ActivityService.create_activity(data.dict())
        return {
            "message": "Activity created successfully",
            "activity_id": activity_id
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Create activity failed: {str(e)}")

# =========================
# ✅ Delete Activity
# =========================
@router.delete("/{activity_id}")
def delete_activity(activity_id: UUID):
    try:
        deleted = ActivityService.delete_activity(str(activity_id))

        if not deleted:
            raise HTTPException(status_code=404, detail="Activity not found")

        return {"message": "Activity deleted successfully"}

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Delete failed: {str(e)}"
        )

# =========================
# ✅ Get All Activities
# =========================
@router.get("/")
def get_all_activities():
    try:
        activities = ActivityService.get_all_activities()
        return {"data": activities}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fetch activities failed: {str(e)}")


# =========================
# ✅ Get Activity By ID
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
# ✅ Update Activity
# =========================
@router.put("/{activity_id}")
def update_activity(activity_id: UUID, data: ActivityUpdate):
    try:
        updated = ActivityService.update_activity(
            activity_id=str(activity_id),
            data=data.dict(exclude_none=True)
        )

        if not updated:
            raise HTTPException(status_code=404, detail="Activity not found")

        return {"message": "Activity updated successfully"}

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")
@router.get("/by-provider/{provider_id}")
def get_activities_by_provider(provider_id: str):
    try:
        activities = ActivityService.get_activities_by_provider(provider_id)
        return activities

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch provider activities: {str(e)}"
        )
