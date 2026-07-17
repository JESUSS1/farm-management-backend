from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)

from app.core.database import db_connection
from app.schemas.user import (
    UserCreate,
    UserPasswordUpdate,
    UserResponse,
    UserUpdate,
)
from app.services.users_service import (
    change_user_password,
    create_user,
    delete_user,
    get_user,
    list_users,
    update_user,
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    return user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_user(
    user_data: UserCreate,
    conn=Depends(db_connection),
):
    try:
        return create_user(
            conn,
            user_data,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.patch(
    "/{usuario_id}",
    response_model=UserResponse,
)
def update_existing_user(
    usuario_id: int,
    user_data: UserUpdate,
    conn=Depends(db_connection),
):
    try:
        user = update_user(
            conn,
            usuario_id,
            user_data,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    return user


@router.patch(
    "/{usuario_id}/password",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_existing_user_password(
    usuario_id: int,
    password_data: UserPasswordUpdate,
    conn=Depends(db_connection),
):
    updated = change_user_password(
        conn,
        usuario_id,
        password_data.password,
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )


@router.delete(
    "/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_user(
    usuario_id: int,
    conn=Depends(db_connection),
):
    deleted = delete_user(
        conn,
        usuario_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )