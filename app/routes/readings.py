from fastapi import APIRouter
from app.db import get_connection
from app.core.database import db_connection
from app.services.readings_service import (list_latest_readings,list_readings,
    list_readings_by_device,
)
from typing import List
from app.schemas.reading import ReadingResponse

router = APIRouter(prefix="/readings", tags=["readings"])

def format_reading(row):
    return {
        "id": row["id"],
        "fecha": row["fecha"],
        "device_id": row["device_id"],
        "sensor": row["sensor"],
        "variable": row["variable"],
        "valor": float(row["valor"]) if row["valor"] is not None else None,
        "unidad": row["unidad"],
        "firmware_version": row["firmware_version"],
    }

@router.get("/latest", response_model=List[ReadingResponse])
def latest_readings():
    with db_connection() as conn:
        rows = list_latest_readings(conn)
    return [format_reading(row) for row in rows]


@router.get("", response_model=List[ReadingResponse])
def readings(limit: int = 50):
    with db_connection() as conn:
        rows = list_readings(conn, limit)
    return [format_reading(row) for row in rows]


@router.get("/{device_id}", response_model=List[ReadingResponse])
def readings_by_device(device_id: str, limit: int = 50):
    with db_connection() as conn:
            rows = list_readings_by_device(conn, device_id, limit)
    return [format_reading(row) for row in rows]
