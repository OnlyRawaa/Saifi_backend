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
            # ✅ لازم واحد منهم موجود
            if not data.get("email") and not data.get("phone"):
                raise ValueError("Email or phone is required")

            # ✅ تحقق من التكرار (إيميل أو جوال)
            cur.execute("""
                SELECT provider_id 
                FROM providers 
                WHERE (%s IS NOT NULL AND email = %s)
                   OR (%s IS NOT NULL AND phone = %s);
            """, (
                data.get("email"), data.get("email"),
                data.get("phone"), data.get("phone")
            ))

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
                    address,
                    password_hash
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING provider_id;
            """, (
                data["name"],
                data.get("email"),
                data.get("phone"),
                data["location_lat"],
                data["location_lng"],
                data["address"],
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
    # ✅ LOGIN PROVIDER (EMAIL OR PHONE)
    # =========================
    @staticmethod
    def login_provider(email: str = None, phone: str = None, password: str = None):
        conn = get_connection()
        cur = conn.cursor()

        try:
            if not email and not phone:
                return None

            cur.execute("""
                SELECT
                    provider_id,
                    name,
                    email,
                    phone,
                    location_lat,
                    location_lng,
                    address,
                    password_hash
                FROM providers
                WHERE (%s IS NOT NULL AND email = %s)
                   OR (%s IS NOT NULL AND phone = %s);
            """, (email, email, phone, phone))

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
                address=row[6],
                password_hash=row[7]
            )

            # ✅ تحقق كلمة المرور
            if not verify_password(password, provider.password_hash):
                return None

            # ✅ إرجاع Dictionary نظيف متوافق مع Flutter
            return {
                "provider_id": provider.provider_id,
                "name": provider.name,              # ✅ هنا التصحيح القاتل
                "email": provider.email,
                "phone": provider.phone,
                "location_lat": provider.location_lat,
                "location_lng": provider.location_lng,
                "address": provider.address,
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
                    address
                FROM providers;
            """)

            return cur.fetchall()

        finally:
            cur.close()
            conn.close()
    # =========================
    # ✅ GET PROVIDER BY ID
    # =========================
    @staticmethod
    def get_provider_by_id(provider_id: str):
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
                    address
                FROM providers
                WHERE provider_id = %s;
            """, (provider_id,))

            return cur.fetchone()

        finally:
            cur.close()
            conn.close()
