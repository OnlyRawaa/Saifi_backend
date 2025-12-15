from fastapi import APIRouter, HTTPException
from services.activity_service import ActivityService
from schemas.activity_schema import ActivityCreate, ActivityUpdate
from uuid import UUID

router = APIRouter(prefix="/activities", tags=["Activities"])


@router.post("/create")
def add_activity(data: ActivityCreate):
    activity_id = ActivityService.create_activity(data.dict())
    return {
        "message": "Activity created successfully",
        "activity_id": activity_id
    }


@router.get("/")
def get_all_activities():
    activities = ActivityService.get_all_activities()
    return {"data": activities}


# ✅ لازم يكون قبل /{activity_id}
@router.get("/by-provider/{provider_id}")
def get_activities_by_provider(provider_id: str):
    activities = ActivityService.get_activities_by_provider(provider_id)
    return {"data": activities or []}


@router.get("/{activity_id}")
def get_activity_by_id(activity_id: str):
    activity = ActivityService.get_activity_by_id(activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.put("/{activity_id}")
def update_activity(activity_id: UUID, data: ActivityUpdate):
    updated = ActivityService.update_activity(
        activity_id=str(activity_id),
        data=data.dict(exclude_none=True)
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"message": "Activity updated successfully"}


@router.delete("/{activity_id}")
def delete_activity(activity_id: UUID):
    deleted = ActivityService.delete_activity(str(activity_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"message": "Activity deleted successfully"}
