from app.db import get_connection

def db_connection():
    conn = get_connection()

    try:
        yield conn
    finally:
        conn.close()