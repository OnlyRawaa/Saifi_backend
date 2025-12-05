from fastapi import APIRouter, HTTPException
from services.auth_service import AuthService
from schemas.parent_schema import ParentCreate, ParentUpdate, ParentLocationUpdate
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
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )

# =========================
# ✅ Parent Login
# =========================
@router.post("/login")
def login_parent(data: dict):
    identifier = data.get("email") or data.get("phone")
    password = data.get("password")

    if not identifier or not password:
        raise HTTPException(status_code=400, detail="Missing credentials")

    parent = AuthService.authenticate_parent(identifier, password)

    if not parent:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "parent_id": parent["parent_id"],
        "first_name": parent["first_name"],
        "last_name": parent["last_name"]
    }


# =========================
# ✅ Get All Parents
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
# ✅ Update Parent Location  ✅<<< لازم قبل /{parent_id}
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
import uuid
from passlib.context import CryptContext
from db.connection import get_connection
from psycopg2.extras import RealDictCursor

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    # =========================
    # ✅ SAVE PARENT
    # =========================
    @staticmethod
    def save_parent(first_name, last_name, email, phone, raw_password):
        conn = get_connection()
        cur = conn.cursor()

        parent_id = str(uuid.uuid4())
        hashed_password = AuthService.hash_password(raw_password)

        try:
            cur.execute(
                "SELECT parent_id FROM parents WHERE email = %s OR phone = %s",
                (email, phone)
            )
            if cur.fetchone():
                raise ValueError("Email or phone already exists")

            cur.execute("""
                INSERT INTO parents 
                (parent_id, first_name, last_name, email, phone, password_hash)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                parent_id,
                first_name,
                last_name,
                email,
                phone,
                hashed_password
            ))

            conn.commit()
            return parent_id

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cur.close()
            conn.close()

    # =========================
    # ✅ AUTHENTICATE PARENT (FIXED)
    # =========================
    @staticmethod
    def authenticate_parent(identifier: str, password: str):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            SELECT * FROM parents
            WHERE email = %s OR phone = %s
        """, (identifier, identifier))

        parent = cur.fetchone()

        cur.close()
        conn.close()

        if not parent:
            return None

        # ✅ تحقق بكلمة المرور الصحيحة باستخدام passlib
        if not AuthService.verify_password(password, parent["password_hash"]):
            return None

        return parent
