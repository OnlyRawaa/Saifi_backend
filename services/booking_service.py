from db.connection import get_connection
from psycopg2.extras import RealDictCursor


class BookingService:

    # =========================
    # ✅ Create Booking
    # =========================
    @staticmethod
    def create_booking(parent_id: str, child_id: str, activity_id: str, provider_id: str):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO bookings (parent_id, child_id, activity_id, provider_id)
            VALUES (%s, %s, %s, %s)
            RETURNING booking_id;
        """, (parent_id, child_id, activity_id, provider_id))

        booking_id = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        return booking_id


    # =========================
    # ✅ Get Parent Bookings
    # =========================
    @staticmethod
    def get_parent_bookings(parent_id: str):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            SELECT
                b.booking_id,
                b.parent_id,
                b.child_id,
                b.activity_id,
                b.provider_id,
                b.status,
                b.booking_date,

                c.first_name || ' ' || c.last_name AS child_name,
                a.title AS activity_title,
                a.price AS price,
                a.type AS type

            FROM bookings b
            JOIN children c ON b.child_id = c.child_id
            JOIN activities a ON b.activity_id = a.activity_id
            WHERE b.parent_id = %s
            ORDER BY b.created_at DESC;
        """, (parent_id,))

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return rows


    # =========================
    # ✅ Get Child Bookings
    # =========================
    @staticmethod
    def get_child_bookings(child_id: str):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            SELECT 
                booking_id,
                parent_id,
                child_id,
                activity_id,
                provider_id,
                status,
                booking_date,
                created_at
            FROM bookings
            WHERE child_id = %s
            ORDER BY created_at DESC;
        """, (child_id,))

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return rows


    # =========================
    # ✅ Update Booking Status
    # =========================
    @staticmethod
    def update_booking_status(booking_id: str, status: str):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE bookings
            SET status = %s
            WHERE booking_id = %s;
        """, (status, booking_id))

        conn.commit()
        cur.close()
        conn.close()

        return True
