from psycopg2.extras import RealDictCursor


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
            EXISTS(
                SELECT 1
                FROM usuario_granja AS ug
                WHERE ug.usuario_id = u.usuario_id
                  AND ug.es_propietario = TRUE
                  AND ug.eliminado_at IS NULL
            ) AS es_propietario,
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
            EXISTS(
                SELECT 1
                FROM usuario_granja AS ug
                WHERE ug.usuario_id = u.usuario_id
                  AND ug.es_propietario = TRUE
                  AND ug.eliminado_at IS NULL
            ) AS es_propietario,
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


def get_user_farm_memberships(
    conn,
    usuario_id: int,
) -> list[dict]:
    query = """
        SELECT
            ug.usuario_granja_id,
            ug.granja_id,
            g.nombre AS granja_nombre,
            ug.rol_granja_id,
            rg.nombre AS rol_granja_nombre,
            ug.es_propietario,
            ug.estado
        FROM usuario_granja AS ug
        INNER JOIN granja AS g
            ON g.granja_id = ug.granja_id
        INNER JOIN rol_granja AS rg
            ON rg.rol_granja_id = ug.rol_granja_id
        WHERE ug.usuario_id = %s
          AND ug.eliminado_at IS NULL
          AND g.eliminado_at IS NULL
          AND rg.eliminado_at IS NULL
          AND ug.estado = TRUE
        ORDER BY ug.es_propietario DESC, ug.usuario_granja_id ASC;
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            query,
            (usuario_id,),
        )

        return cursor.fetchall()


def get_farm_role_permission_codes(
    conn,
    rol_granja_id: int,
) -> list[str]:
    query = """
        SELECT
            p.codigo
        FROM rol_granja_permiso AS rgp
        INNER JOIN permiso AS p
            ON p.permiso_id = rgp.permiso_id
        WHERE rgp.rol_granja_id = %s
          AND rgp.eliminado_at IS NULL
          AND p.eliminado_at IS NULL
          AND rgp.estado = TRUE
        ORDER BY p.permiso_id;
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            query,
            (rol_granja_id,),
        )

        return [row["codigo"] for row in cursor.fetchall()]
