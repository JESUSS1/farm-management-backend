from psycopg2.extras import RealDictCursor

from app.core.exceptions import (
    FarmRoleNotFoundException,
    FarmNotFoundException,
    UserNotFoundException,
    FarmRolePermissionAlreadyExistsException,
)


def usuario_exists(conn, usuario_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            SELECT EXISTS(
                SELECT 1
                FROM usuario
                WHERE usuario_id = %s
                    AND eliminado_at IS NULL
            ) AS existe;
            """,
            (usuario_id,),
        )

        result = cursor.fetchone()

        return result["existe"]


def farm_exists(conn, granja_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            SELECT EXISTS(
                SELECT 1
                FROM granja
                WHERE granja_id = %s
                    AND eliminado_at IS NULL
            ) AS existe;
            """,
            (granja_id,),
        )

        result = cursor.fetchone()

        return result["existe"]


def farm_role_exists(conn, rol_granja_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            SELECT EXISTS(
                SELECT 1
                FROM rol_granja
                WHERE rol_granja_id = %s
                    AND eliminado_at IS NULL
            ) AS existe;
            """,
            (rol_granja_id,),
        )

        result = cursor.fetchone()

        return result["existe"]


def get_farm_user(conn, usuario_granja_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            SELECT
                usuario_granja_id,
                usuario_id,
                granja_id,
                rol_granja_id,
                es_propietario,
                estado,
                created_at,
                updated_at
            FROM usuario_granja
            WHERE usuario_granja_id = %s
                AND eliminado_at IS NULL;
            """,
            (usuario_granja_id,),
        )

        return cursor.fetchone()


def get_farm_users(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""
            SELECT
                usuario_granja_id,
                usuario_id,
                granja_id,
                rol_granja_id,
                es_propietario,
                estado,
                created_at,
                updated_at
            FROM usuario_granja
            WHERE eliminado_at IS NULL
            ORDER BY usuario_granja_id;
            """)

        return cursor.fetchall()


def create_farm_user_record(conn, usuario_id, granja_id, rol_granja_id, es_propietario):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO usuario_granja (
                    usuario_id,
                    granja_id,
                    rol_granja_id,
                    es_propietario
                )
                VALUES (%s, %s, %s, %s)
                RETURNING usuario_granja_id;
                """,
                (
                    usuario_id,
                    granja_id,
                    rol_granja_id,
                    es_propietario,
                ),
            )

            result = cursor.fetchone()

            return result["usuario_granja_id"]

    except Exception as exc:
        conn.rollback()
        raise


def update_farm_user_record(conn, usuario_granja_id, data):
    if not data:
        return

    columns = []
    values = []

    for key, value in data.items():
        columns.append(f"{key} = %s")
        values.append(value)

    values.append(usuario_granja_id)

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            f"""
            UPDATE usuario_granja
            SET {', '.join(columns)}
            WHERE usuario_granja_id = %s
                AND eliminado_at IS NULL;
            """,
            tuple(values),
        )

        return cursor.rowcount


def soft_delete_farm_user(conn, usuario_granja_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            UPDATE usuario_granja
            SET eliminado_at = CURRENT_TIMESTAMP,
                estado = FALSE
            WHERE usuario_granja_id = %s
                AND eliminado_at IS NULL;
            """,
            (usuario_granja_id,),
        )

        return cursor.rowcount
