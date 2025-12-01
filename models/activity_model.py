def create_activity(
    conn,
    provider_id,
    title,
    description,
    price,
    gender,
    age_from,
    age_to,
    start_date,
    end_date,
    capacity=0,
    duration=0,
    status=True
):
    try:
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO activities (
                provider_id,
                title,
                description,
                price,
                gender,
                age_from,
                age_to,
                start_date,
                end_date,
                capacity,
                duration,
                status,
                created_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            RETURNING activity_id;
        """, (
            provider_id,
            title,
            description,
            price,
            gender,
            age_from,
            age_to,
            start_date,
            end_date,
            capacity,
            duration,
            status
        ))

        activity_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return activity_id

    except Exception as e:
        conn.rollback()
        raise e
