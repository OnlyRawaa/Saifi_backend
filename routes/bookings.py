from fastapi import APIRouter, HTTPException
from services.booking_service import BookingService
from schemas.booking_schema import BookingCreate, BookingUpdate
from uuid import UUID

router = APIRouter(prefix="/bookings", tags=["Bookings"])


# =========================
# ✅ Create Booking (FROM FLUTTER) ✅✅✅
# =========================
@router.post("")
def create_booking(data: BookingCreate):
    try:
        booking_id = BookingService.create_booking(
            parent_id=str(data.parent_id),
            child_id=str(data.child_id),
            activity_id=str(data.activity_id),
            provider_id=str(data.provider_id),
            booking_date=data.booking_date,
            start_date=data.start_date,
            end_date=data.end_date,
            notes=data.notes
        )

        return {
            "message": "Booking created successfully",
            "booking_id": booking_id
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Create booking failed: {str(e)}"
        )


# =========================
# ✅ Delete Booking (PARENT)
# =========================
@router.delete("/{booking_id}")
def delete_booking(booking_id: UUID):
    try:
        BookingService.delete_booking(str(booking_id))
        return {"message": "Booking deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
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
        result = BookingService.get_bookings_by_activity(str(activity_id))
        print("BOOKINGS RESULT 👉", result)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Fetch activity bookings failed: {str(e)}"
        )


