def create_child(
    conn,
    parent_id,
    fname,
    lname,
    birthdate,
    age,
    interests,
    gender=None,
    notes=None
):
    try:
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO children (
                parent_id,
                first_name,
                last_name,
                birthdate,
                age,
                interests,
                gender,
                notes,
                created_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
            RETURNING child_id;
        """, (
            parent_id,
            fname,
            lname,
            birthdate,
            age,
            interests,
            gender,
            notes
        ))

        child_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return child_id

    except Exception as e:
        conn.rollback()
        raise e
