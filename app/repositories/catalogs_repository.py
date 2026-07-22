from psycopg2.extras import RealDictCursor


def get_system_roles(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""
            SELECT
                rol_sistema_id,
                nombre,
                descripcion,
                estado
            FROM rol_sistema
            WHERE eliminado_at IS NULL
            ORDER BY rol_sistema_id;
            """)

        return cursor.fetchall()


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
