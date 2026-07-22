from psycopg2.extras import RealDictCursor
from psycopg2.errors import UniqueViolation

from app.core.exceptions import (
    FarmNotFoundException,
    FarmRoleAlreadyExistsException,
)


def get_farm_role(conn, farm_role_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            SELECT
                rol_granja_id,
                granja_id,
                nombre,
                descripcion,
                estado,
                created_at,
                updated_at
            FROM rol_granja
            WHERE rol_granja_id = %s
                AND eliminado_at IS NULL;
            """,
            (farm_role_id,),
        )

        return cursor.fetchone()


def get_farm_roles(conn, search=None, granja_id=None, limit=50, offset=0):
    query = """
        SELECT
            rol_granja_id,
            granja_id,
            nombre,
            descripcion,
            estado,
            created_at,
            updated_at
        FROM rol_granja
        WHERE eliminado_at IS NULL
    """
    params = []

    if granja_id is not None:
        query += " AND granja_id = %s"
        params.append(granja_id)

    if search:
        query += """
            AND (
                LOWER(nombre) LIKE LOWER(%s)
                OR LOWER(COALESCE(descripcion, '')) LIKE LOWER(%s)
            )
        """
        pattern = f"%{search}%"
        params.extend([pattern] * 2)

    query += " ORDER BY rol_granja_id LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(query, params)

        return cursor.fetchall()


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


def create_farm_role_record(conn, granja_id, nombre, descripcion):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO rol_granja (
                    granja_id,
                    nombre,
                    descripcion
                )
                VALUES (%s, %s, %s)
                RETURNING rol_granja_id;
                """,
                (
                    granja_id,
                    nombre,
                    descripcion,
                ),
            )

            result = cursor.fetchone()

            return result["rol_granja_id"]

    except UniqueViolation as exc:
        conn.rollback()

        raise RolGranjaAlreadyExistsException() from exc


def update_farm_role_record(conn, farm_role_id, data):
    if not data:
        return

    columns = []
    values = []
    index = 1

    for key, value in data.items():
        columns.append(f"{key} = %s")
        values.append(value)
        index += 1

    values.append(farm_role_id)

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            f"""
            UPDATE rol_granja
            SET {', '.join(columns)}
            WHERE rol_granja_id = %s
                AND eliminado_at IS NULL;
            """,
            tuple(values),
        )

        return cursor.rowcount


def soft_delete_farm_role(conn, farm_role_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            UPDATE rol_granja
            SET eliminado_at = CURRENT_TIMESTAMP,
                estado = FALSE
            WHERE rol_granja_id = %s
                AND eliminado_at IS NULL;
            """,
            (farm_role_id,),
        )

        return cursor.rowcount
