from app.core.exceptions import FarmNotFoundException
from app.repositories.farms_repository import (
    create_farm_record,
    get_farm,
    get_farms,
    soft_delete_farm,
    update_farm_record,
)


def list_farms(conn):
    return get_farms(conn)


def get_farm_by_id(conn, granja_id):
    farm = get_farm(conn, granja_id)

    if farm is None:
        raise FarmNotFoundException()

    return farm


def create_farm(conn, farm_data):
    farm_id = create_farm_record(
        conn,
        farm_data.nombre.strip(),
        farm_data.ubicacion,
        farm_data.descripcion,
    )

    conn.commit()

    return get_farm(conn, farm_id)


def update_farm(conn, granja_id, farm_data):
    farm = get_farm(conn, granja_id)

    if farm is None:
        raise FarmNotFoundException()

    data = farm_data.model_dump(exclude_unset=True)

    if "nombre" in data and data["nombre"] is not None:
        data["nombre"] = data["nombre"].strip()

    update_farm_record(
        conn,
        granja_id,
        data,
    )

    conn.commit()

    return get_farm(conn, granja_id)


def delete_farm(conn, granja_id):
    farm = get_farm(conn, granja_id)

    if farm is None:
        raise FarmNotFoundException()

    soft_delete_farm(
        conn,
        granja_id,
    )

    conn.commit()

    return granja_id
