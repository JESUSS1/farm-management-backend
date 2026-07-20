from app.core.database import get_connection


def open_connection():
    conn = get_connection()

    if conn is None:
        raise RuntimeError("No fue posible conectar con la base de datos.")

    return conn
