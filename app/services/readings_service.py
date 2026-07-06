from app.repositories.readings_repository import (
    get_latest_readings,
    get_readings,
    get_readings_by_device,
)


def list_latest_readings(conn):
    return get_latest_readings(conn)


def list_readings(conn, limit: int = 50):
    return get_readings(conn, limit)


def list_readings_by_device(conn, device_id: str, limit: int = 50):
    return get_readings_by_device(conn, device_id, limit)