from app.core.exceptions import (
    InactiveUserException,
    InvalidCredentialsException,
)
from app.core.jwt import create_access_token
from app.core.security import verify_password
from app.repositories.auth_repository import (
    get_user_for_authentication,
)
from app.schemas.auth import LoginRequest


def authenticate_user(
    conn,
    login_data: LoginRequest,
) -> dict:
    """
    Valida las credenciales del usuario y genera un access token JWT.
    """

    user = get_user_for_authentication(
        conn,
        login_data.username,
    )

    if user is None:
        raise InvalidCredentialsException()

    if not verify_password(
        login_data.password,
        user["password_hash"],
    ):
        raise InvalidCredentialsException()

    if not user["estado"]:
        raise InactiveUserException()

    access_token = create_access_token(
        subject=str(user["usuario_id"])
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }