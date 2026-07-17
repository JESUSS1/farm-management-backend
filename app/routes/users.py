from fastapi import APIRouter, Depends, HTTPException

from app.core.database import db_connection
from app.schemas.user import UserResponse
from app.services.users_service import (
    get_user,
    list_users,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/",
    response_model=list[UserResponse],
)
def get_users(conn=Depends(db_connection)):
    return list_users(conn)


@router.get(
    "/{usuario_id}",
    response_model=UserResponse,
)
def get_user_by_id(
    usuario_id: int,
    conn=Depends(db_connection),
):
    user = get_user(conn, usuario_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado",
        )

    return user