from fastapi import APIRouter, Depends

from app.core.auth import get_current_user
from app.core.database import db_connection
from app.schemas.auth import (
    AuthenticatedUserResponse,
    LoginRequest,
    TokenResponse,
)
from app.services.auth_service import authenticate_user
router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    login_data: LoginRequest,
    conn=Depends(db_connection),
):
    return authenticate_user(
        conn,
        login_data,
    )


@router.get(
    "/me",
    response_model=AuthenticatedUserResponse,
)
def get_authenticated_user(
    current_user: dict = Depends(get_current_user),
):
    return current_user