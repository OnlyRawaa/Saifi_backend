import uuid
from passlib.context import CryptContext
from db.connection import get_connection
from psycopg2.extras import RealDictCursor

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    # =========================
    # ✅ HASH / VERIFY
    # =========================
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
    # ✅ GET PARENT BY ID (مع اللوكيشن)
    # =========================
    @staticmethod
    def get_parent_by_id(parent_id: str):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT parent_id, first_name, last_name, email, phone,
                   location_lat, location_lng, created_at
            FROM parents
            WHERE parent_id = %s
        """, (parent_id,))

        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            return None

        return {
            "parent_id": str(row[0]),
            "first_name": row[1],
            "last_name": row[2],
            "email": row[3],
            "phone": row[4],
            "location_lat": row[5],
            "location_lng": row[6],
            "created_at": row[7],
        }

    # =========================
    # ✅ AUTHENTICATE PARENT
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

        if not AuthService.verify_password(password, parent["password_hash"]):
            return None

        return parent

    # =========================
    # ✅ UPDATE PARENT (البيانات الأساسية)
    # =========================
    @staticmethod
    def update_parent(parent_id: str, data: dict):
        conn = get_connection()
        cur = conn.cursor()

        if not data:
            return False

        fields = []
        values = []

        for key, value in data.items():
            fields.append(f"{key} = %s")
            values.append(value)

        values.append(parent_id)

        query = f"""
            UPDATE parents
            SET {', '.join(fields)}
            WHERE parent_id = %s
        """

        try:
            cur.execute(query, values)
            conn.commit()
            return cur.rowcount > 0

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cur.close()
            conn.close()

    # =========================
    # ✅ UPDATE PARENT LOCATION
    # =========================
    @staticmethod
    def update_parent_location(parent_id: str, lat: float, lng: float):
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                UPDATE parents
                SET location_lat = %s,
                    location_lng = %s
                WHERE parent_id = %s
            """, (lat, lng, parent_id))

            conn.commit()
            return cur.rowcount > 0

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cur.close()
            conn.close()
