from collections.abc import Callable

from fastapi import Depends
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
from app.core.jwt import decode_access_token
from app.repositories.auth_repository import (
    get_authenticated_user_by_id,
)


bearer_scheme = HTTPBearer(
    auto_error=False,
)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
    conn=Depends(db_connection),
) -> dict:
    """
    Valida el Bearer token y devuelve el usuario autenticado.
    """

    if credentials is None:
        raise InvalidTokenException()

    if credentials.scheme.lower() != "bearer":
        raise InvalidTokenException()

    payload = decode_access_token(
        credentials.credentials
    )

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


require_system_admin = require_roles(
    "SUPERADMIN",
)