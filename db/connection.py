import psycopg2

def get_connection():
    return psycopg2.connect(
        host="172.20.10.3",
        port=5432,
        database="saifi_database",
        user="saifi_database_user",
        password="bGXelz6hZPxjugFrjv1SCoPnw1uEzruh"
    )
