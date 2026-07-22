from psycopg2.extras import RealDictCursor


def get_farm(conn, granja_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            SELECT
                granja_id,
                nombre,
                ubicacion,
                descripcion,
                estado,
                created_at,
                updated_at
            FROM granja
            WHERE granja_id = %s
                AND eliminado_at IS NULL;
            """,
            (granja_id,),
        )

        return cursor.fetchone()


def get_farms(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""
            SELECT
                granja_id,
                nombre,
                ubicacion,
                descripcion,
                estado,
                created_at,
                updated_at
            FROM granja
            WHERE eliminado_at IS NULL
            ORDER BY granja_id;
            """)

        return cursor.fetchall()


def create_farm_record(conn, nombre, ubicacion, descripcion):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            INSERT INTO granja (
                nombre,
                ubicacion,
                descripcion
            )
            VALUES (%s, %s, %s)
            RETURNING granja_id;
            """,
            (
                nombre,
                ubicacion,
                descripcion,
            ),
        )

        result = cursor.fetchone()

        return result["granja_id"]


def update_farm_record(conn, granja_id, data):
    if not data:
        return

    columns = []
    values = []

    for key, value in data.items():
        columns.append(f"{key} = %s")
        values.append(value)

    values.append(granja_id)

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            f"""
            UPDATE granja
            SET {', '.join(columns)}
            WHERE granja_id = %s
                AND eliminado_at IS NULL;
            """,
            tuple(values),
        )

        return cursor.rowcount


def soft_delete_farm(conn, granja_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            UPDATE granja
            SET eliminado_at = CURRENT_TIMESTAMP,
                estado = FALSE
            WHERE granja_id = %s
                AND eliminado_at IS NULL;
            """,
            (granja_id,),
        )

        return cursor.rowcount
