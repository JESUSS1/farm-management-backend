from typing import List

from fastapi import APIRouter, Depends

from app.core.auth import get_current_user, require_permissions
from app.core.database import db_connection
from app.schemas.schedule import ScheduleCreate, ScheduleResponse, ScheduleUpdate
from app.services.schedules_service import (
    add_schedule,
    edit_schedule,
    list_schedules,
    remove_schedule,
)

router = APIRouter(
    prefix="/schedules",
    tags=["Schedules"],
    dependencies=[Depends(get_current_user)],
)


def format_schedule(row):
    return {
        "id": row["id"],
        "nombre": row["nombre"],
        "hora": str(row["hora"]),
        "funcion": row["funcion"],
        "target": row["target"],
        "activo": row["activo"],
        "ultima_ejecucion": row["ultima_ejecucion"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


@router.get("", response_model=List[ScheduleResponse])
def schedules(
    current_user: dict = Depends(require_permissions("SCHEDULES_VIEW")),
    conn=Depends(db_connection),
):
    rows = list_schedules(conn)
    return [format_schedule(row) for row in rows]


@router.post("")
def create(
    schedule: ScheduleCreate,
    current_user: dict = Depends(require_permissions("SCHEDULES_CREATE")),
    conn=Depends(db_connection),
):
    new_id = add_schedule(conn, schedule)

    return {
        "message": "Horario creado",
        "id": new_id,
    }


@router.put("/{schedule_id}")
def update(
    schedule_id: int,
    schedule: ScheduleUpdate,
    current_user: dict = Depends(require_permissions("SCHEDULES_UPDATE")),
    conn=Depends(db_connection),
):
    updated_id = edit_schedule(conn, schedule_id, schedule)

    if updated_id is None:
        return {"message": "Horario no encontrado"}

    return {
        "message": "Horario actualizado",
        "id": updated_id,
    }


@router.delete("/{schedule_id}")
def delete(
    schedule_id: int,
    current_user: dict = Depends(require_permissions("SCHEDULES_DELETE")),
    conn=Depends(db_connection),
):
    deleted_id = remove_schedule(conn, schedule_id)

    if deleted_id is None:
        return {"message": "Horario no encontrado"}

    return {
        "message": "Horario eliminado",
        "id": deleted_id,
    }
