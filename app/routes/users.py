from fastapi import (
    APIRouter,
    Depends,
    Query,
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
from app.core.auth import require_system_admin

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[
        Depends(require_system_admin),
    ],
)


@router.get(
    "/",
    response_model=list[UserResponse],
)
def get_users(
    conn=Depends(db_connection),
    search: str | None = None,
    rol_sistema_id: int | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return list_users(
        conn,
        search=search,
        rol_sistema_id=rol_sistema_id,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{usuario_id}",
    response_model=UserResponse,
)
def get_user_by_id(
    usuario_id: int,
    conn=Depends(db_connection),
):
    return get_user(
        conn,
        usuario_id,
    )


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_user(
    user_data: UserCreate,
    conn=Depends(db_connection),
):
    return create_user(
        conn,
        user_data,
    )


@router.patch(
    "/{usuario_id}",
    response_model=UserResponse,
)
def update_existing_user(
    usuario_id: int,
    user_data: UserUpdate,
    conn=Depends(db_connection),
):
    return update_user(
        conn,
        usuario_id,
        user_data,
    )


@router.patch(
    "/{usuario_id}/password",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_existing_user_password(
    usuario_id: int,
    password_data: UserPasswordUpdate,
    conn=Depends(db_connection),
):
    change_user_password(
        conn,
        usuario_id,
        password_data.password,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )


@router.delete(
    "/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_user(
    usuario_id: int,
    conn=Depends(db_connection),
):
    delete_user(
        conn,
        usuario_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
