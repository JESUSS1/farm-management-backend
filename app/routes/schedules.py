from fastapi import APIRouter
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate
from app.core.database import db_connection
from app.services.schedules_service import (
    list_schedules,
    add_schedule,
    edit_schedule,
    remove_schedule,
)
from typing import List
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate, ScheduleResponse

router =  APIRouter(prefix="/schedules", tags=["schedules"])


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
def schedules():
    with db_connection() as conn:
        rows = list_schedules(conn)
        return [format_schedule(row) for row in rows]
      


@router.post("")
def create(schedule: ScheduleCreate):
        with db_connection() as conn:
            new_id = add_schedule(conn, schedule)
        return {
            "message": "Horario creado",
            "id": new_id,
        }


@router.put("/{schedule_id}")
def update(schedule_id: int, schedule: ScheduleUpdate):
        with db_connection() as conn:
            updated_id = edit_schedule(conn, schedule_id, schedule)

        if updated_id is None:
            return {"message": "Horario no encontrado"}

        return {
            "message": "Horario actualizado",
            "id": updated_id,
        }


@router.delete("/{schedule_id}")
def delete(schedule_id: int):
        with db_connection() as conn:
            deleted_id = remove_schedule(conn, schedule_id)

        if deleted_id is None:
            return {"message": "Horario no encontrado"}

        return {
            "message": "Horario eliminado",
            "id": deleted_id,
        }