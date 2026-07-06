from contextlib import contextmanager
from app.db import get_connection


@contextmanager
def db_connection():
    conn = get_connection()

    try:
        yield conn
    finally:
        conn.close()