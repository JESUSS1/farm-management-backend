from app.core.exceptions import (
    FarmNotFoundException,
    FarmRoleNotFoundException,
)
from app.repositories.farm_roles_repository import (
    create_farm_role_record,
    get_farm_role,
    get_farm_roles,
    farm_exists,
    soft_delete_farm_role,
    update_farm_role_record,
)


def list_farm_roles(conn, search=None, granja_id=None, limit=50, offset=0):
    return get_farm_roles(
        conn,
        search=search,
        granja_id=granja_id,
        limit=limit,
        offset=offset,
    )


def get_farm_role_by_id(conn, farm_role_id):
    farm_role = get_farm_role(conn, farm_role_id)

    if farm_role is None:
        raise FarmRoleNotFoundException()

    return farm_role


def create_farm_role(conn, farm_role_data):
    if not farm_exists(conn, farm_role_data.granja_id):
        raise FarmNotFoundException()

    farm_role_id = create_farm_role_record(
        conn,
        farm_role_data.granja_id,
        farm_role_data.nombre.strip(),
        farm_role_data.descripcion,
    )

    conn.commit()

    return get_farm_role(conn, farm_role_id)


def update_farm_role(conn, farm_role_id, farm_role_data):
    farm_role = get_farm_role(conn, farm_role_id)

    if farm_role is None:
        raise FarmRoleNotFoundException()

    data = farm_role_data.model_dump(exclude_unset=True)

    if "nombre" in data:
        data["nombre"] = data["nombre"].strip()

    update_farm_role_record(
        conn,
        farm_role_id,
        data,
    )

    conn.commit()

    return get_farm_role(conn, farm_role_id)


def delete_farm_role(conn, farm_role_id):
    farm_role = get_farm_role(conn, farm_role_id)

    if farm_role is None:
        raise FarmRoleNotFoundException()

    soft_delete_farm_role(
        conn,
        farm_role_id,
    )

    conn.commit()

    return farm_role_id
