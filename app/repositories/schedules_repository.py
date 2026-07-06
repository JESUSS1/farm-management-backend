def get_schedules(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, nombre, hora, funcion, target, activo,  created_at, updated_at
            FROM horario_funciones
            ORDER BY hora ASC;
            """
        )
        return cursor.fetchall()


def create_schedule(conn, schedule):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO horario_funciones
            (nombre, hora, funcion, target, activo)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (schedule.nombre, schedule.hora, schedule.funcion, schedule.target, schedule.activo),
        )
        new_id = cursor.fetchone()[0]

    conn.commit()
    return new_id


def update_schedule(conn, schedule_id, schedule):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            UPDATE horario_funciones
            SET
                nombre = COALESCE(%s, nombre),
                hora = COALESCE(%s, hora),
                funcion = COALESCE(%s, funcion),
                target = COALESCE(%s, target),
                activo = COALESCE(%s, activo),
                updated_at = NOW()
            WHERE id = %s
            RETURNING id;
            """,
            (schedule.nombre, schedule.hora, schedule.funcion, schedule.target, schedule.activo, schedule_id),
        )
        row = cursor.fetchone(),
    

    conn.commit()
    return row[0] if row else None


def delete_schedule(conn, schedule_id):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM horario_funciones
            WHERE id = %s
            RETURNING id;
            """,
            (schedule_id,),
        )
        row = cursor.fetchone()

    conn.commit()
    return row[0] if row else None