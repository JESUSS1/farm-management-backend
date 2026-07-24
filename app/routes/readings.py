from typing import List

from fastapi import APIRouter, Depends

from app.core.auth import get_current_user, require_permissions
from app.core.database import db_connection
from app.services.readings_service import (
    list_latest_readings,
    list_readings,
    list_readings_by_device,
)
from app.schemas.reading import ReadingResponse

router = APIRouter(
    prefix="/readings",
    tags=["Readings"],
    dependencies=[Depends(get_current_user)],
)


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
def latest_readings(
    current_user: dict = Depends(require_permissions("SENSOR_READINGS_VIEW")),
    conn=Depends(db_connection),
):
    rows = list_latest_readings(conn)

    return [format_reading(row) for row in rows]


@router.get("", response_model=List[ReadingResponse])
def readings(
    limit: int = 50,
    current_user: dict = Depends(require_permissions("SENSOR_READINGS_VIEW")),
    conn=Depends(db_connection),
):
    rows = list_readings(conn, limit)

    return [format_reading(row) for row in rows]


@router.get("/{device_id}", response_model=List[ReadingResponse])
def readings_by_device(
    device_id: str,
    limit: int = 50,
    current_user: dict = Depends(require_permissions("SENSOR_READINGS_VIEW")),
    conn=Depends(db_connection),
):
    rows = list_readings_by_device(conn, device_id, limit)

    return [format_reading(row) for row in rows]
