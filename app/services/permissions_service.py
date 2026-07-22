from app.core.exceptions import (
    PermissionNotFoundException,
)
from app.repositories.permissions_repository import (
    create_permission_record,
    get_permission_by_id,
    get_permissions,
)


def list_permissions(conn):
    return get_permissions(conn)


def get_permission(conn, permiso_id):
    permission = get_permission_by_id(
        conn,
        permiso_id,
    )

    if permission is None:
        raise PermissionNotFoundException()

    return permission


def create_permission(
    conn,
    permission_data,
):
    permiso_id = create_permission_record(
        conn,
        permission_data.codigo,
        permission_data.nombre,
        permission_data.descripcion,
    )

    conn.commit()

    return get_permission(
        conn,
        permiso_id,
    )


from app.repositories.permissions_repository import (
    create_permission_record,
    get_permission_by_code,
    get_permission_by_id,
    get_permissions,
)


def create_permission_if_not_exists(
    conn,
    permission,
) -> bool:
    """
    Crea el permiso únicamente si no existe.

    Retorna:
        True  -> si fue creado.
        False -> si ya existía.
    """

    exists = get_permission_by_code(
        conn,
        permission.code,
    )

    if exists:
        return False

    create_permission_record(
        conn,
        permission.code,
        permission.name,
        permission.description,
    )

    return True
