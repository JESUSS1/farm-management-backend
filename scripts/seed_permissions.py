from app.constants.permissions import (
    PERMISSIONS,
)

from app.core.database import (
    get_connection,
)

from app.services.permissions_service import (
    create_permission_if_not_exists,
)

from scripts.console import (
    print_summary,
)


def seed_permissions():

    conn = get_connection()

    inserted = 0
    skipped = 0

    try:

        for permission in PERMISSIONS:

            created = create_permission_if_not_exists(
                conn,
                permission,
            )

            if created:
                inserted += 1
            else:
                skipped += 1

        conn.commit()

        print_summary(
            "PERMISSIONS",
            inserted,
            skipped,
        )

    except Exception:

        conn.rollback()
        raise

    finally:

        conn.close()


if __name__ == "__main__":
    seed_permissions()
