from fastapi import APIRouter, HTTPException
from services.booking_service import BookingService
from schemas.booking_schema import BookingCreate, BookingUpdate
from uuid import UUID

router = APIRouter(prefix="/bookings", tags=["Bookings"])


# =========================
# ✅ Create Booking (FROM FLUTTER)
# =========================
@router.post("/")
def create_booking(data: BookingCreate):
    try:
        booking = BookingService.create_booking(data.model_dump())

        return {
            "message": "Booking created successfully",
            "booking": booking
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Create booking failed: {str(e)}"
        )


# =========================
# ✅ Get All Bookings By Parent
# =========================
@router.get("/parent/{parent_id}")
def get_parent_bookings(parent_id: UUID):
    try:
        return BookingService.get_parent_bookings(str(parent_id))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Fetch parent bookings failed: {str(e)}"
        )


# =========================
# ✅ Get All Bookings By Child
# =========================
@router.get("/child/{child_id}")
def get_child_bookings(child_id: UUID):
    try:
        return BookingService.get_child_bookings(str(child_id))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Fetch child bookings failed: {str(e)}"
        )


# =========================
# ✅ Update Booking Status (PROVIDER)
# =========================
@router.put("/{booking_id}/status")
def update_booking_status(booking_id: UUID, data: BookingUpdate):
    try:
        updated = BookingService.update_booking_status(
            str(booking_id),
            data.status
        )

        if not updated:
            raise HTTPException(status_code=404, detail="Booking not found")

        return {"message": "Booking status updated successfully"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Update booking failed: {str(e)}"
        )


# =========================
# ✅ Get All Bookings By Activity (FOR PROVIDER)
# =========================
@router.get("/activity/{activity_id}")
def get_bookings_by_activity(activity_id: UUID):
    try:
        return BookingService.get_bookings_by_activity(str(activity_id))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Fetch activity bookings failed: {str(e)}"
        )
