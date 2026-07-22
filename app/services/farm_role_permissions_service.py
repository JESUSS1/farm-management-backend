from app.core.exceptions import (
    FarmRoleNotFoundException,
    FarmRolePermissionNotFoundException,
    PermissionNotFoundException,
)
from app.repositories.farm_role_permissions_repository import (
    create_farm_role_permission_record,
    get_farm_role_permission,
    get_farm_role_permissions,
    soft_delete_farm_role_permission,
    update_farm_role_permission_record,
)
from app.repositories.farm_roles_repository import get_farm_role
from app.repositories.permissions_repository import get_permission_by_id


def list_farm_role_permissions(conn):
    return get_farm_role_permissions(conn)


def get_farm_role_permission_by_id(conn, farm_role_permission_id):
    farm_role_permission = get_farm_role_permission(
        conn,
        farm_role_permission_id,
    )

    if farm_role_permission is None:
        raise FarmRolePermissionNotFoundException()

    return farm_role_permission


def create_farm_role_permission(conn, data):
    if get_farm_role(conn, data.farm_role_id) is None:
        raise FarmRoleNotFoundException()

    if get_permission_by_id(conn, data.permission_id) is None:
        raise PermissionNotFoundException()

    farm_role_permission_id = create_farm_role_permission_record(
        conn,
        data.farm_role_id,
        data.permission_id,
    )

    conn.commit()

    return get_farm_role_permission(conn, farm_role_permission_id)


def update_farm_role_permission(conn, farm_role_permission_id, data):
    farm_role_permission = get_farm_role_permission(
        conn,
        farm_role_permission_id,
    )

    if farm_role_permission is None:
        raise FarmRolePermissionNotFoundException()

    updated_data = data.model_dump(exclude_unset=True)

    update_farm_role_permission_record(
        conn,
        farm_role_permission_id,
        updated_data,
    )

    conn.commit()

    return get_farm_role_permission(conn, farm_role_permission_id)


def delete_farm_role_permission(conn, farm_role_permission_id):
    farm_role_permission = get_farm_role_permission(
        conn,
        farm_role_permission_id,
    )

    if farm_role_permission is None:
        raise FarmRolePermissionNotFoundException()

    soft_delete_farm_role_permission(
        conn,
        farm_role_permission_id,
    )

    conn.commit()

    return farm_role_permission_id
