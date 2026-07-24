from psycopg2.extras import RealDictCursor
from psycopg2.errors import UniqueViolation

from app.core.exceptions import (
    FarmRolePermissionAlreadyExistsException,
)


def get_farm_role_permission(conn, farm_role_permission_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            SELECT
                rol_granja_permiso_id,
                rol_granja_id,
                permiso_id AS permission_id,
                estado,
                created_at,
                updated_at
            FROM rol_granja_permiso
            WHERE rol_granja_permiso_id = %s
                AND eliminado_at IS NULL;
            """,
            (farm_role_permission_id,),
        )

        return cursor.fetchone()


def get_farm_role_permissions(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""
            SELECT
                rol_granja_permiso_id,
                rol_granja_id,
                permiso_id AS permission_id,
                estado,
                created_at,
                updated_at
            FROM rol_granja_permiso
            WHERE eliminado_at IS NULL
            ORDER BY rol_granja_permiso_id;
            """)

        return cursor.fetchall()


def get_permission_ids_by_farm_role(conn, farm_role_id: int) -> list[int]:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            SELECT
                permiso_id
            FROM rol_granja_permiso
            WHERE rol_granja_id = %s
                AND eliminado_at IS NULL
                AND estado = TRUE
            ORDER BY permiso_id;
            """,
            (farm_role_id,),
        )

        return [row["permiso_id"] for row in cursor.fetchall()]


def create_farm_role_permissions_for_role(
    conn, farm_role_id: int, permission_ids: list[int]
):
    if not permission_ids:
        return

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        for permission_id in permission_ids:
            cursor.execute(
                """
                INSERT INTO rol_granja_permiso (
                    rol_granja_id,
                    permiso_id
                )
                VALUES (%s, %s);
                """,
                (
                    farm_role_id,
                    permission_id,
                ),
            )


def create_farm_role_permission_record(conn, farm_role_id, permission_id):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO rol_granja_permiso (
                    rol_granja_id,
                    permiso_id
                )
                VALUES (%s, %s)
                RETURNING rol_granja_permiso_id;
                """,
                (
                    farm_role_id,
                    permission_id,
                ),
            )

            result = cursor.fetchone()

            return result["rol_granja_permiso_id"]

    except UniqueViolation as exc:
        conn.rollback()

        raise FarmRolePermissionAlreadyExistsException() from exc


def update_farm_role_permission_record(conn, farm_role_permission_id, data):
    if not data:
        return

    columns = []
    values = []

    for key, value in data.items():
        columns.append(f"{key} = %s")
        values.append(value)

    values.append(farm_role_permission_id)

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            f"""
            UPDATE rol_granja_permiso
            SET {', '.join(columns)}
            WHERE rol_granja_permiso_id = %s
                AND eliminado_at IS NULL;
            """,
            tuple(values),
        )

        return cursor.rowcount


def soft_delete_farm_role_permission(conn, farm_role_permission_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            UPDATE rol_granja_permiso
            SET eliminado_at = CURRENT_TIMESTAMP,
                estado = FALSE
            WHERE rol_granja_permiso_id = %s
                AND eliminado_at IS NULL;
            """,
            (farm_role_permission_id,),
        )

        return cursor.rowcount
