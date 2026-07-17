from app.repositories.users_repository import (
    get_users,
    get_user_by_id,
)


def list_users(conn):
    return get_users(conn)


def get_user(conn, usuario_id):
    user = get_user_by_id(conn, usuario_id)

    if user is None:
        return None

    return user