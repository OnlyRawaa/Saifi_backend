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
def get_activity_by_id(activity_id: UUID):
    try:
        activity = ActivityService.get_activity_by_id(str(activity_id))

        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        return {"data": activity}

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fetch activity failed: {str(e)}")


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
