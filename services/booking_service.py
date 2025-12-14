from db.connection import get_connection
from psycopg2.extras import RealDictCursor


class BookingService:

    # =========================
    # ✅ Create Booking
    # =========================
    @staticmethod
    def create_booking(
        parent_id: str,
        child_id: str,
        activity_id: str,
        provider_id: str,
        booking_date,
        start_date=None,
        end_date=None,
        notes=None
    ):
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                INSERT INTO bookings 
                (parent_id, child_id, activity_id, provider_id, status, booking_date, start_date, end_date, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING booking_id;
            """, (
                str(parent_id),
                str(child_id),
                str(activity_id),
                str(provider_id),
                'pending',
                booking_date,
                start_date,
                end_date,
                notes
            ))

            booking_id = cur.fetchone()[0]
            conn.commit()
            return booking_id

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cur.close()
            conn.close()

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
                b.start_date,
                b.end_date,
                b.notes,

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
    # ✅ Delete Booking (PARENT)
    # =========================
    @staticmethod
    def delete_booking(booking_id: str):
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                DELETE FROM bookings
                WHERE booking_id = %s;
            """, (booking_id,))

            affected = cur.rowcount
            conn.commit()

            if affected == 0:
                raise Exception("Booking not found")

            return True

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cur.close()
            conn.close()

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
                start_date,
                end_date,
                notes,
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

        try:
            cur.execute("""
                SELECT activity_id
                FROM bookings
                WHERE booking_id = %s
                AND status = 'pending';
            """, (booking_id,))

            row = cur.fetchone()
            if not row:
                conn.rollback()
                return False

            activity_id = row[0]

            cur.execute("""
                SELECT capacity
                FROM activities
                WHERE activity_id = %s
                FOR UPDATE;
            """, (activity_id,))

            capacity_row = cur.fetchone()
            if not capacity_row:
                conn.rollback()
                return False

            capacity = capacity_row[0]

            if status == "approved":
                if capacity <= 0:
                    conn.rollback()
                    raise ValueError("No remaining capacity for this activity")

                cur.execute("""
                    UPDATE bookings
                    SET status = 'approved'
                    WHERE booking_id = %s;
                """, (booking_id,))

                cur.execute("""
                    UPDATE activities
                    SET capacity = capacity - 1
                    WHERE activity_id = %s;
                """, (activity_id,))

            elif status == "rejected":
                cur.execute("""
                    UPDATE bookings
                    SET status = 'rejected'
                    WHERE booking_id = %s;
                """, (booking_id,))

            else:
                conn.rollback()
                raise ValueError("Invalid status value")

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cur.close()
            conn.close()

    # =========================
    # ✅ Get Bookings By Activity (FOR PROVIDER)
    # =========================
    @staticmethod
    def get_bookings_by_activity(activity_id: str):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            SELECT
                b.booking_id,
                b.status,
                b.booking_date,
                b.created_at,

                c.first_name || ' ' || c.last_name AS child_name,
                c.gender AS child_gender,
                c.age AS child_age,

                p.first_name || ' ' || p.last_name AS parent_name,
                p.phone AS parent_phone

            FROM bookings b
            JOIN children c ON b.child_id = c.child_id
            JOIN parents p ON b.parent_id = p.parent_id
            WHERE b.activity_id = %s
            ORDER BY b.created_at DESC;
        """, (activity_id,))

        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
