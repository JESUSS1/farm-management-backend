from psycopg2.extras import RealDictCursor


def get_users(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            SELECT
                u.usuario_id,
                u.username,
                u.email,
                u.estado,
                rs.rol_sistema_id,
                rs.nombre AS rol_sistema,
                p.persona_id,
                p.nombres,
                p.apellidos,
                p.telefono,
                p.documento_identidad,
                u.created_at,
                u.updated_at
            FROM usuario u
            INNER JOIN rol_sistema rs
                ON rs.rol_sistema_id = u.rol_sistema_id
            LEFT JOIN persona p
                ON p.usuario_id = u.usuario_id
            WHERE u.eliminado_at IS NULL
            ORDER BY u.usuario_id;
            """
        )

        return cursor.fetchall()

def get_user_by_id(conn, usuario_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            SELECT
                u.usuario_id,
                u.username,
                u.email,
                u.estado,
                rs.rol_sistema_id,
                rs.nombre AS rol_sistema,
                p.persona_id,
                p.nombres,
                p.apellidos,
                p.telefono,
                p.documento_identidad,
                u.created_at,
                u.updated_at
            FROM usuario u
            INNER JOIN rol_sistema rs
                ON rs.rol_sistema_id = u.rol_sistema_id
            LEFT JOIN persona p
                ON p.usuario_id = u.usuario_id
            WHERE
                u.usuario_id = %s
                AND u.eliminado_at IS NULL;
            """,
            (usuario_id,),
        )

        return cursor.fetchone()
    
def get_user_by_username(conn, username):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            SELECT
                usuario_id,
                rol_sistema_id,
                username,
                password_hash,
                email,
                estado
            FROM usuario
            WHERE
                username = %s
                AND eliminado_at IS NULL;
            """,
            (username,),
        )

        return cursor.fetchone()
