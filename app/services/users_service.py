from app.core.security import hash_password
from app.repositories.users_repository import (
    create_person_record,
    create_user_record,
    get_user_by_email,
    get_user_by_id,
    get_user_by_username,
    get_users,
    role_exists,
    soft_delete_user,
    update_person_record,
    update_user_password,
    update_user_record,
)


def list_users(conn):
    return get_users(conn)


def get_user(conn, usuario_id):
    return get_user_by_id(conn, usuario_id)


def create_user(conn, user_data):
    username = user_data.username.strip()
    email = (
        str(user_data.email).strip().lower()
        if user_data.email
        else None
    )

    nombres = user_data.nombres.strip()
    apellidos = user_data.apellidos.strip()

    if not role_exists(conn, user_data.rol_sistema_id):
        raise ValueError("El rol del sistema no existe")

    if get_user_by_username(conn, username):
        raise ValueError("El nombre de usuario ya está registrado")

    if email and get_user_by_email(conn, email):
        raise ValueError("El correo electrónico ya está registrado")

    password_hash = hash_password(user_data.password)

    try:
        usuario_id = create_user_record(
            conn=conn,
            rol_sistema_id=user_data.rol_sistema_id,
            username=username,
            password_hash=password_hash,
            email=email,
        )

        create_person_record(
            conn=conn,
            usuario_id=usuario_id,
            nombres=nombres,
            apellidos=apellidos,
            telefono=user_data.telefono,
            documento_identidad=user_data.documento_identidad,
        )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    return get_user_by_id(conn, usuario_id)


def update_user(conn, usuario_id, user_data):
    current_user = get_user_by_id(conn, usuario_id)

    if current_user is None:
        return None

    data = user_data.model_dump(exclude_unset=True)

    non_nullable_fields = {
        "rol_sistema_id",
        "username",
        "nombres",
        "apellidos",
        "estado",
    }

    for field in non_nullable_fields:
        if field in data and data[field] is None:
            raise ValueError(
                f"El campo '{field}' no puede ser nulo"
            )

    if "rol_sistema_id" in data:
        if not role_exists(conn, data["rol_sistema_id"]):
            raise ValueError("El rol del sistema no existe")

    if "username" in data:
        data["username"] = data["username"].strip()

        existing_user = get_user_by_username(
            conn,
            data["username"],
        )

        if (
            existing_user
            and existing_user["usuario_id"] != usuario_id
        ):
            raise ValueError(
                "El nombre de usuario ya está registrado"
            )

    if "email" in data:
        data["email"] = (
            str(data["email"]).strip().lower()
            if data["email"]
            else None
        )

        if data["email"]:
            existing_email = get_user_by_email(
                conn,
                data["email"],
            )

            if (
                existing_email
                and existing_email["usuario_id"] != usuario_id
            ):
                raise ValueError(
                    "El correo electrónico ya está registrado"
                )

    if "nombres" in data:
        data["nombres"] = data["nombres"].strip()

    if "apellidos" in data:
        data["apellidos"] = data["apellidos"].strip()

    try:
        update_user_record(
            conn,
            usuario_id,
            data,
        )

        update_person_record(
            conn,
            usuario_id,
            data,
        )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    return get_user_by_id(conn, usuario_id)


def change_user_password(
    conn,
    usuario_id,
    password,
):
    user = get_user_by_id(conn, usuario_id)

    if user is None:
        return False

    password_hash = hash_password(password)

    try:
        updated = update_user_password(
            conn,
            usuario_id,
            password_hash,
        )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    return updated


def delete_user(conn, usuario_id):
    user = get_user_by_id(conn, usuario_id)

    if user is None:
        return False

    try:
        deleted = soft_delete_user(
            conn,
            usuario_id,
        )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    return deleted