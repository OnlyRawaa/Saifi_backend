import psycopg2

def get_connection():
    return psycopg2.connect(
        host="dpg-d44bclk9c44c73ca7950-a",
        port=5432,
        database="saifi_db",
        user="saifi_db_user",
        password="Pwnxb4A2O6Ev268G8fash5b5OkV5l7v8"
    )
