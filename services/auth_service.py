import uuid
from passlib.context import CryptContext
from db.connection import get_connection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    # =========================
    # ✅ HASH PASSWORD
    # =========================
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    # =========================
    # ✅ VERIFY PASSWORD
    # =========================
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    # =========================
    # ✅ SAVE PARENT (REGISTER)
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
    # ✅ GET ALL PARENTS
    # =========================
    @staticmethod
    def get_all_parents():
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT parent_id, first_name, last_name, email, phone, created_at
            FROM parents
            ORDER BY created_at DESC
        """)

        rows = cur.fetchall()
        cur.close()
        conn.close()

        result = []
        for r in rows:
            result.append({
                "parent_id": str(r[0]),
                "first_name": r[1],
                "last_name": r[2],
                "email": r[3],
                "phone": r[4],
                "created_at": r[5]
            })

        return result

    # =========================
    # ✅ UPDATE PARENT
    # =========================
    @staticmethod
    def update_parent(parent_id: str, data: dict):
        conn = get_connection()
        cur = conn.cursor()

        fields = []
        values = []

        for key, value in data.items():
            fields.append(f"{key} = %s")
            values.append(value)

        if not fields:
            cur.close()
            conn.close()
            return False

        values.append(parent_id)

        try:
            cur.execute(f"""
                UPDATE parents
                SET {', '.join(fields)}
                WHERE parent_id = %s
            """, tuple(values))

            if cur.rowcount == 0:
                return False

            conn.commit()
            return True

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
                WHERE parent_id = %s;
            """, (lat, lng, parent_id))

            updated = cur.rowcount
            conn.commit()
            return updated > 0

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cur.close()
            conn.close()
@staticmethod
def authenticate_parent(identifier: str, password: str):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    query = """
        SELECT * FROM parents
        WHERE email = %s OR phone = %s
    """
    cur.execute(query, (identifier, identifier))
    parent = cur.fetchone()

    if not parent:
        return None

    stored_hash = parent["password_hash"].encode()
    if not bcrypt.checkpw(password.encode(), stored_hash):
        return None

    return parent
