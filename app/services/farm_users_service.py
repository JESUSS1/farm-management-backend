from app.core.exceptions import (
    FarmNotFoundException,
    FarmRoleNotFoundException,
    UserNotFoundException,
    FarmRolePermissionAlreadyExistsException,
)
from app.repositories.farm_users_repository import (
    create_farm_user_record,
    farm_exists,
    farm_role_exists,
    get_farm_user,
    get_farm_users,
    soft_delete_farm_user,
    update_farm_user_record,
    usuario_exists,
)


def list_farm_users(conn):
    return get_farm_users(conn)


def get_farm_user_by_id(conn, usuario_granja_id):
    farm_user = get_farm_user(conn, usuario_granja_id)

    if farm_user is None:
        raise UserNotFoundException()

    return farm_user


def create_farm_user(conn, data):
    if not usuario_exists(conn, data.usuario_id):
        raise UserNotFoundException()

    if not farm_exists(conn, data.granja_id):
        raise FarmNotFoundException()

    if not farm_role_exists(conn, data.rol_granja_id):
        raise FarmRoleNotFoundException()

    usuario_granja_id = create_farm_user_record(
        conn,
        data.usuario_id,
        data.granja_id,
        data.rol_granja_id,
        data.es_propietario,
    )

    conn.commit()

    return get_farm_user(conn, usuario_granja_id)


def update_farm_user(conn, usuario_granja_id, data):
    farm_user = get_farm_user(conn, usuario_granja_id)

    if farm_user is None:
        raise UserNotFoundException()

    updated_data = data.model_dump(exclude_unset=True)

    if "rol_granja_id" in updated_data:
        if not farm_role_exists(conn, updated_data["rol_granja_id"]):
            raise FarmRoleNotFoundException()

    update_farm_user_record(
        conn,
        usuario_granja_id,
        updated_data,
    )

    conn.commit()

    return get_farm_user(conn, usuario_granja_id)


def delete_farm_user(conn, usuario_granja_id):
    farm_user = get_farm_user(conn, usuario_granja_id)

    if farm_user is None:
        raise UserNotFoundException()

    soft_delete_farm_user(
        conn,
        usuario_granja_id,
    )

    conn.commit()

    return usuario_granja_id
