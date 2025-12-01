from db.connection import get_connection
from psycopg2.extras import RealDictCursor
from utils.hashing import hash_password, verify_password
from models.provider_model import Provider


class ProviderService:

    # =========================
    # ✅ REGISTER PROVIDER
    # =========================
    @staticmethod
    def register_provider(data: dict):
        conn = get_connection()
        cur = conn.cursor()

        try:
            # ✅ تحقق من التكرار (إيميل أو جوال)
            cur.execute(
                "SELECT provider_id FROM providers WHERE email = %s OR phone = %s;",
                (data["email"], data["phone"])
            )
            if cur.fetchone():
                raise ValueError("Email or phone already exists")

            hashed = hash_password(data["password"])

            cur.execute("""
                INSERT INTO providers (
                    name,
                    email,
                    phone,
                    location_lat,
                    location_lng,
                    description,
                    password_hash
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING provider_id;
            """, (
                data["name"],
                data["email"],
                data["phone"],
                data["location_lat"],
                data["location_lng"],
                data["description"],
                hashed
            ))

            provider_id = cur.fetchone()[0]
            conn.commit()

            return {"provider_id": provider_id}

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cur.close()
            conn.close()

    # =========================
    # ✅ LOGIN PROVIDER
    # =========================
    @staticmethod
    def login_provider(email: str, password: str):
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT
                    provider_id,
                    name,
                    email,
                    phone,
                    location_lat,
                    location_lng,
                    description,
                    password_hash
                FROM providers
                WHERE email = %s;
            """, (email,))

            row = cur.fetchone()

            if not row:
                return None

            provider = Provider(
                provider_id=row[0],
                name=row[1],
                email=row[2],
                phone=row[3],
                location_lat=row[4],
                location_lng=row[5],
                description=row[6],
                password_hash=row[7]
            )

            # ✅ تحقق كلمة المرور
            if not verify_password(password, provider.password_hash):
                return None

            # ✅ نرجع بيانات نظيفة للـ API
            return {
                "provider_id": provider.provider_id,
                "name": provider.name,
                "email": provider.email,
                "phone": provider.phone,
                "location_lat": provider.location_lat,
                "location_lng": provider.location_lng,
                "description": provider.description
            }

        finally:
            cur.close()
            conn.close()

    # =========================
    # ✅ GET ALL PROVIDERS
    # =========================
    @staticmethod
    def get_all_providers():
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute("""
                SELECT
                    provider_id,
                    name,
                    email,
                    phone,
                    location_lat,
                    location_lng,
                    description
                FROM providers;
            """)

            return cur.fetchall()

        finally:
            cur.close()
            conn.close()
