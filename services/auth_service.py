import uuid
from passlib.context import CryptContext
from db.connection import get_connection   

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def save_parent(first_name, last_name, email, phone, raw_password):
        conn = get_connection()
        cur = conn.cursor()

        # توليد UUID حقيقي
        parent_id = str(uuid.uuid4())

        # تشفير كلمة المرور
        hashed_password = AuthService.hash_password(raw_password)

        try:
            # ✅ التحقق من التكرار
            cur.execute(
                "SELECT id FROM parents WHERE email = %s OR phone = %s",
                (email, phone)
            )
            if cur.fetchone():
                raise ValueError("Email or phone already exists")

            # ✅ الإدخال
            cur.execute("""
                INSERT INTO parents (id, first_name, last_name, email, phone, password)
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
