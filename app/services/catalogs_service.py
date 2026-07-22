from app.repositories.catalogs_repository import (
    get_permissions,
    get_system_roles,
)


def list_system_roles(conn):
    return get_system_roles(conn)


def list_permissions(conn):
    return get_permissions(conn)
