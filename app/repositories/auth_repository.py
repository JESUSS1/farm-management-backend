def get_user_for_authentication(
    conn,
    username: str,
) -> dict | None:
    query = """
        SELECT
            u.usuario_id,
            u.username,
            u.password_hash,
            u.rol_sistema_id,
            rs.nombre AS rol_nombre,
            u.estado
        FROM usuario AS u
        INNER JOIN rol_sistema AS rs
            ON rs.rol_sistema_id = u.rol_sistema_id
        WHERE u.username = %s
          AND u.eliminado_at IS NULL
          AND rs.eliminado_at IS NULL;
    """

    with conn.cursor() as cursor:
        cursor.execute(
            query,
            (username,),
        )

        return cursor.fetchone()
    
    
def get_authenticated_user_by_id(
    conn,
    usuario_id: int,
) -> dict | None:
    query = """
        SELECT
            u.usuario_id,
            u.username,
            u.rol_sistema_id,
            rs.nombre AS rol_nombre,
            u.estado
        FROM usuario AS u
        INNER JOIN rol_sistema AS rs
            ON rs.rol_sistema_id = u.rol_sistema_id
        WHERE u.usuario_id = %s
          AND u.eliminado_at IS NULL
          AND rs.eliminado_at IS NULL;
    """

    with conn.cursor() as cursor:
        cursor.execute(
            query,
            (usuario_id,),
        )

        return cursor.fetchone()