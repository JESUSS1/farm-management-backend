from psycopg2.errors import UniqueViolation
from psycopg2.extras import RealDictCursor

from app.core.exceptions import (
    PermissionCodeAlreadyExistsException,
)


def get_permissions(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""
            SELECT
                permiso_id,
                codigo,
                nombre,
                descripcion,
                estado
            FROM permiso
            WHERE eliminado_at IS NULL
            ORDER BY permiso_id;
            """)

        return cursor.fetchall()


def get_permission_by_id(conn, permiso_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            SELECT
                permiso_id,
                codigo,
                nombre,
                descripcion,
                estado
            FROM permiso
            WHERE
                permiso_id = %s
                AND eliminado_at IS NULL;
            """,
            (permiso_id,),
        )

        return cursor.fetchone()


def get_permission_by_code(conn, codigo):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            SELECT
                permiso_id,
                codigo,
                nombre,
                descripcion,
                estado
            FROM permiso
            WHERE
                LOWER(codigo) = LOWER(%s)
                AND eliminado_at IS NULL;
            """,
            (codigo,),
        )

        return cursor.fetchone()


def create_permission_record(
    conn,
    codigo,
    nombre,
    descripcion,
):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO permiso (
                    codigo,
                    nombre,
                    descripcion
                )
                VALUES (%s, %s, %s)
                RETURNING permiso_id;
                """,
                (
                    codigo,
                    nombre,
                    descripcion,
                ),
            )

            result = cursor.fetchone()

            return result["permiso_id"]

    except UniqueViolation as exc:
        conn.rollback()

        if exc.diag.constraint_name == "permiso_codigo_key":
            raise PermissionCodeAlreadyExistsException() from exc

        raise
