def get_latest_readings(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT DISTINCT ON (device_id, sensor, variable)
                id, fecha, device_id, sensor, variable, valor, unidad, firmware_version
            FROM lecturas_sensor
            ORDER BY device_id, sensor, variable, fecha DESC;
            """
        )

        return cursor.fetchall()


def get_readings(conn, limit: int = 50):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, fecha, device_id, sensor, variable, valor, unidad, firmware_version
            FROM lecturas_sensor
            ORDER BY fecha DESC
            LIMIT %s;
            """,
            (limit,),
        )

        return cursor.fetchall()


def get_readings_by_device(conn, device_id: str, limit: int = 50):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, fecha, device_id, sensor, variable, valor, unidad, firmware_version
            FROM lecturas_sensor
            WHERE device_id = %s
            ORDER BY fecha DESC
            LIMIT %s;
            """,
            (device_id, limit),
        )

        return cursor.fetchall()