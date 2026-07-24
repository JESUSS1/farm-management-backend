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
from app.repositories.farm_role_permissions_repository import (
    create_farm_role_permissions_for_role,
    get_permission_ids_by_farm_role,
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


def clone_farm_role(conn, source_farm_role_id, clone_data):
    source_farm_role = get_farm_role(conn, source_farm_role_id)

    if source_farm_role is None:
        raise FarmRoleNotFoundException()

    if not farm_exists(conn, clone_data.granja_id):
        raise FarmNotFoundException()

    clone_name = (
        clone_data.nombre.strip()
        if clone_data.nombre is not None
        else source_farm_role["nombre"]
    )

    clone_description = (
        clone_data.descripcion
        if "descripcion" in clone_data.model_fields_set
        else source_farm_role["descripcion"]
    )

    permission_ids = get_permission_ids_by_farm_role(
        conn,
        source_farm_role_id,
    )

    try:
        cloned_farm_role_id = create_farm_role_record(
            conn,
            clone_data.granja_id,
            clone_name,
            clone_description,
        )

        create_farm_role_permissions_for_role(
            conn,
            cloned_farm_role_id,
            permission_ids,
        )

        conn.commit()
    except Exception:
        conn.rollback()
        raise

    return get_farm_role(conn, cloned_farm_role_id)
