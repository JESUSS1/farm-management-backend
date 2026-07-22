from psycopg2.extras import RealDictCursor
from psycopg2.errors import UniqueViolation
from app.core.exceptions import (
    EmailAlreadyExistsException,
    UsernameAlreadyExistsException,
)


def get_users(conn, search=None, rol_sistema_id=None, limit=50, offset=0):
    query = """
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
    """
    params = []

    if search:
        query += """
            AND (
                LOWER(u.username) LIKE LOWER(%s)
                OR LOWER(COALESCE(u.email, '')) LIKE LOWER(%s)
                OR LOWER(COALESCE(p.nombres, '')) LIKE LOWER(%s)
                OR LOWER(COALESCE(p.apellidos, '')) LIKE LOWER(%s)
            )
        """
        pattern = f"%{search}%"
        params.extend([pattern] * 4)

    if rol_sistema_id is not None:
        query += " AND u.rol_sistema_id = %s"
        params.append(rol_sistema_id)

    query += " ORDER BY u.usuario_id LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(query, params)

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
                LOWER(username) = LOWER(%s)
                AND eliminado_at IS NULL;
            """,
            (username,),
        )

        return cursor.fetchone()


def get_user_by_email(conn, email):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            SELECT
                usuario_id,
                username,
                email
            FROM usuario
            WHERE
                LOWER(email) = LOWER(%s)
                AND eliminado_at IS NULL;
            """,
            (email,),
        )

        return cursor.fetchone()


def role_exists(conn, rol_sistema_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            SELECT EXISTS(
                SELECT 1
                FROM rol_sistema
                WHERE rol_sistema_id = %s
            ) AS existe;
            """,
            (rol_sistema_id,),
        )

        result = cursor.fetchone()

        return result["existe"]


def count_active_superadmins(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""
            SELECT COUNT(*) AS count
            FROM usuario u
            INNER JOIN rol_sistema rs
                ON rs.rol_sistema_id = u.rol_sistema_id
            WHERE rs.nombre = 'SUPERADMIN'
                AND u.estado = TRUE
                AND u.eliminado_at IS NULL;
            """)

        result = cursor.fetchone()

        return result["count"]


def create_user_record(
    conn,
    rol_sistema_id,
    username,
    password_hash,
    email,
):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO usuario (
                    rol_sistema_id,
                    username,
                    password_hash,
                    email
                )
                VALUES (%s, %s, %s, %s)
                RETURNING usuario_id;
                """,
                (
                    rol_sistema_id,
                    username,
                    password_hash,
                    email,
                ),
            )

            result = cursor.fetchone()

            return result["usuario_id"]

    except UniqueViolation as exc:
        conn.rollback()

        constraint_name = exc.diag.constraint_name

        if constraint_name == "usuario_username_key":
            raise UsernameAlreadyExistsException() from exc

        if constraint_name == "usuario_email_key":
            raise EmailAlreadyExistsException() from exc

        raise


def create_person_record(
    conn,
    usuario_id,
    nombres,
    apellidos,
    telefono,
    documento_identidad,
):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO persona (
                usuario_id,
                nombres,
                apellidos,
                telefono,
                documento_identidad
            )
            VALUES (%s, %s, %s, %s, %s);
            """,
            (
                usuario_id,
                nombres,
                apellidos,
                telefono,
                documento_identidad,
            ),
        )


def update_user_record(conn, usuario_id, data):
    allowed_fields = {
        "rol_sistema_id",
        "username",
        "email",
        "estado",
    }

    fields = {key: value for key, value in data.items() if key in allowed_fields}

    if not fields:
        return

    assignments = [f"{field} = %s" for field in fields]

    values = list(fields.values())
    values.append(usuario_id)

    with conn.cursor() as cursor:
        cursor.execute(
            f"""
            UPDATE usuario
            SET
                {", ".join(assignments)},
                updated_at = CURRENT_TIMESTAMP
            WHERE
                usuario_id = %s
                AND eliminado_at IS NULL;
            """,
            values,
        )


def update_person_record(conn, usuario_id, data):
    allowed_fields = {
        "nombres",
        "apellidos",
        "telefono",
        "documento_identidad",
    }

    fields = {key: value for key, value in data.items() if key in allowed_fields}

    if not fields:
        return

    assignments = [f"{field} = %s" for field in fields]

    values = list(fields.values())
    values.append(usuario_id)

    with conn.cursor() as cursor:
        cursor.execute(
            f"""
            UPDATE persona
            SET {", ".join(assignments)}
            WHERE usuario_id = %s;
            """,
            values,
        )


def update_user_password(conn, usuario_id, password_hash):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            UPDATE usuario
            SET
                password_hash = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE
                usuario_id = %s
                AND eliminado_at IS NULL;
            """,
            (
                password_hash,
                usuario_id,
            ),
        )

        return cursor.rowcount > 0


def soft_delete_user(conn, usuario_id):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            UPDATE usuario
            SET
                estado = FALSE,
                eliminado_at = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
            WHERE
                usuario_id = %s
                AND eliminado_at IS NULL;
            """,
            (usuario_id,),
        )

        return cursor.rowcount > 0
