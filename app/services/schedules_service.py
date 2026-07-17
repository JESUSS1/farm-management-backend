from fastapi import HTTPException
from app.repositories.schedules_repository import (
    get_schedules,
    create_schedule,
    update_schedule,
    delete_schedule,
)


VALID_FUNCTIONS = ["OPEN", "CLOSE", "STATUS","ENCENDER_LED","APAGAR_LED"]


def validate_schedule_data(schedule):
    if schedule.nombre is not None and not schedule.nombre.strip():
        raise HTTPException(status_code=400, detail="El nombre no puede estar vacío")

    if schedule.target is not None and not schedule.target.strip():
        raise HTTPException(status_code=400, detail="El target no puede estar vacío")

    if schedule.funcion is not None:
        funcion = schedule.funcion.strip().upper()

        if funcion not in VALID_FUNCTIONS:
            raise HTTPException(
                status_code=400,
                detail="Función inválida. Use OPEN, CLOSE o STATUS",
            )

        schedule.funcion = funcion

    if schedule.target is not None:
        schedule.target = schedule.target.strip()

    if schedule.nombre is not None:
        schedule.nombre = schedule.nombre.strip()


def list_schedules(conn):
    return get_schedules(conn)


def add_schedule(conn, schedule):
    validate_schedule_data(schedule)
    return create_schedule(conn, schedule)


def edit_schedule(conn, schedule_id, schedule):
    validate_schedule_data(schedule)
    return update_schedule(conn, schedule_id, schedule)


def remove_schedule(conn, schedule_id):
    return delete_schedule(conn, schedule_id)