from collections.abc import Callable

from fastapi import Depends, Header
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from app.core.database import db_connection
from app.core.exceptions import (
    InactiveUserException,
    InvalidTokenException,
    UserNotFoundException,
    ForbiddenException,
)
from app.constants.permissions import PERMISSIONS
from app.core.jwt import decode_access_token
from app.repositories.auth_repository import (
    get_farm_role_permission_codes,
    get_authenticated_user_by_id,
    get_user_farm_memberships,
)

SUPERADMIN_ROLE_NAME = "SUPERADMIN"
CLIENT_ROLE_NAME = "CLIENTE"

OWNER_PERMISSION_CODES = {
    "FARMS_VIEW",
    "FARMS_CREATE",
    "FARMS_UPDATE",
    "FARMS_DELETE",
    "AREAS_VIEW",
    "AREAS_CREATE",
    "AREAS_UPDATE",
    "AREAS_DELETE",
    "ROLES_VIEW",
    "ROLES_CREATE",
    "ROLES_UPDATE",
    "ROLES_DELETE",
    "PERMISSIONS_VIEW",
    "PERMISSIONS_CREATE",
    "PERMISSIONS_UPDATE",
    "PERMISSIONS_DELETE",
    "FARM_USERS_VIEW",
    "FARM_USERS_ASSIGN",
    "FARM_USERS_UPDATE",
    "FARM_USERS_REMOVE",
    "DEVICES_VIEW",
    "DEVICES_CREATE",
    "DEVICES_UPDATE",
    "DEVICES_DELETE",
    "DEVICES_CONTROL",
    "SENSORS_VIEW",
    "SENSORS_CONFIGURE",
    "TASKS_VIEW",
    "TASKS_CREATE",
    "TASKS_UPDATE",
    "TASKS_DELETE",
    "TASKS_EXECUTE",
    "SCHEDULES_VIEW",
    "SCHEDULES_CREATE",
    "SCHEDULES_UPDATE",
    "SCHEDULES_DELETE",
    "SENSOR_READINGS_VIEW",
    "REPORTS_VIEW",
    "REPORTS_EXPORT",
}


def build_effective_permissions(user: dict) -> list[str]:
    role_name = (user.get("rol_nombre") or "").upper()

    if role_name == SUPERADMIN_ROLE_NAME:
        return [permission.code for permission in PERMISSIONS]

    if role_name == CLIENT_ROLE_NAME and user.get("es_propietario"):
        return [
            permission.code
            for permission in PERMISSIONS
            if permission.code in OWNER_PERMISSION_CODES
        ]

    return []


def build_farm_membership_contexts(
    conn,
    usuario_id: int,
) -> list[dict]:
    memberships = get_user_farm_memberships(conn, usuario_id)

    contexts: list[dict] = []

    for membership in memberships:
        permissions = get_farm_role_permission_codes(
            conn,
            membership["rol_granja_id"],
        )

        contexts.append(
            {
                "usuario_granja_id": membership["usuario_granja_id"],
                "granja_id": membership["granja_id"],
                "granja_nombre": membership["granja_nombre"],
                "rol_granja_id": membership["rol_granja_id"],
                "rol_granja_nombre": membership["rol_granja_nombre"],
                "es_propietario": membership["es_propietario"],
                "estado": membership["estado"],
                "permissions": permissions,
            }
        )

    return contexts


def build_active_farm_context(farm_memberships: list[dict]) -> dict | None:
    if not farm_memberships:
        return None

    for membership in farm_memberships:
        if membership["es_propietario"]:
            return membership

    return farm_memberships[0]


def build_active_farm_context_by_id(
    farm_memberships: list[dict],
    requested_farm_id: int,
) -> dict | None:
    for membership in farm_memberships:
        if membership["granja_id"] == requested_farm_id:
            return membership

    return None


def build_effective_permissions_from_context(
    user: dict,
    active_farm_context: dict | None,
) -> list[str]:
    role_name = (user.get("rol_nombre") or "").upper()

    if role_name == SUPERADMIN_ROLE_NAME:
        return [permission.code for permission in PERMISSIONS]

    if role_name != CLIENT_ROLE_NAME or active_farm_context is None:
        return []

    if active_farm_context["es_propietario"]:
        return [
            permission.code
            for permission in PERMISSIONS
            if permission.code in OWNER_PERMISSION_CODES
        ]

    return active_farm_context["permissions"]


bearer_scheme = HTTPBearer(
    auto_error=False,
)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    x_farm_id: int | None = Header(default=None, alias="X-Farm-Id"),
    conn=Depends(db_connection),
) -> dict:
    """
    Valida el Bearer token y devuelve el usuario autenticado.
    """

    if credentials is None:
        raise InvalidTokenException()

    if credentials.scheme.lower() != "bearer":
        raise InvalidTokenException()

    payload = decode_access_token(credentials.credentials)

    subject = payload.get("sub")

    if subject is None:
        raise InvalidTokenException()

    try:
        usuario_id = int(subject)
    except (TypeError, ValueError) as exc:
        raise InvalidTokenException() from exc

    user = get_authenticated_user_by_id(
        conn,
        usuario_id,
    )

    if user is None:
        raise UserNotFoundException()

    if not user["estado"]:
        raise InactiveUserException()

    farm_memberships = build_farm_membership_contexts(
        conn,
        user["usuario_id"],
    )

    requested_farm_context = None
    if x_farm_id is not None:
        requested_farm_context = build_active_farm_context_by_id(
            farm_memberships,
            x_farm_id,
        )

        if (
            requested_farm_context is None
            and user.get("rol_nombre") != SUPERADMIN_ROLE_NAME
        ):
            raise ForbiddenException(
                detail="No tienes acceso a la granja solicitada",
            )

    active_farm_context = requested_farm_context or build_active_farm_context(
        farm_memberships
    )

    user["active_farm_id"] = (
        x_farm_id
        if user.get("rol_nombre") == SUPERADMIN_ROLE_NAME and x_farm_id is not None
        else (active_farm_context["granja_id"] if active_farm_context else None)
    )
    user["farm_memberships"] = farm_memberships
    user["permissions"] = build_effective_permissions_from_context(
        user,
        active_farm_context,
    )

    return user


def require_roles(
    *allowed_roles: str,
) -> Callable:
    """
    Crea una dependencia que permite el acceso únicamente
    a los roles indicados.
    """

    def role_checker(
        current_user: dict = Depends(get_current_user),
    ) -> dict:
        role_name = current_user.get("rol_nombre")

        if role_name not in allowed_roles:
            raise ForbiddenException()

        return current_user

    return role_checker


def require_permissions(
    *required_permissions: str,
) -> Callable:
    def permission_checker(
        current_user: dict = Depends(get_current_user),
    ) -> dict:
        role_name = (current_user.get("rol_nombre") or "").upper()

        if role_name == SUPERADMIN_ROLE_NAME:
            return current_user

        current_permissions = set(current_user.get("permissions") or [])
        missing_permissions = [
            permission
            for permission in required_permissions
            if permission not in current_permissions
        ]

        if missing_permissions:
            raise ForbiddenException(
                detail=(
                    "No tienes permisos para realizar esta acción. "
                    f"Permisos requeridos: {', '.join(required_permissions)}"
                )
            )

        return current_user

    return permission_checker


require_system_admin = require_roles(
    "SUPERADMIN",
)
