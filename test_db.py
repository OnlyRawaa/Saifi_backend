import psycopg2

try:
    conn = psycopg2.connect(
        host="172.20.10.3",
        port=5432,
        database="saifi_database",
        user="saifi_database_user",
        password="bGXelz6hZPxjugFrjv1SCoPnw1uEzruh",
        connect_timeout=5
    )
    print("✅ Connection successful")
    conn.close()

except Exception as e:
    print("❌ Connection failed:")
    print(e)
