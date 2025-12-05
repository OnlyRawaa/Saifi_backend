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
