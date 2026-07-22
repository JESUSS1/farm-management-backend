from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from app.core.auth import get_current_user
from app.core.database import db_connection
from app.schemas.farm_user import (
    FarmUserCreate,
    FarmUserResponse,
    FarmUserUpdate,
)
from app.services.farm_users_service import (
    create_farm_user,
    delete_farm_user,
    get_farm_user_by_id,
    list_farm_users,
    update_farm_user,
)

router = APIRouter(
    prefix="/farm-users",
    tags=["FarmUsers"],
    dependencies=[
        Depends(get_current_user),
    ],
)


@router.get(
    "/",
    response_model=list[FarmUserResponse],
)
def get_farm_users(
    conn=Depends(db_connection),
):
    return list_farm_users(conn)


@router.get(
    "/{usuario_granja_id}",
    response_model=FarmUserResponse,
)
def get_farm_user(
    usuario_granja_id: int,
    conn=Depends(db_connection),
):
    return get_farm_user_by_id(conn, usuario_granja_id)


@router.post(
    "/",
    response_model=FarmUserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_farm_user(
    farm_user_data: FarmUserCreate,
    conn=Depends(db_connection),
):
    return create_farm_user(conn, farm_user_data)


@router.patch(
    "/{usuario_granja_id}",
    response_model=FarmUserResponse,
)
def update_existing_farm_user(
    usuario_granja_id: int,
    farm_user_data: FarmUserUpdate,
    conn=Depends(db_connection),
):
    return update_farm_user(conn, usuario_granja_id, farm_user_data)


@router.delete(
    "/{usuario_granja_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_farm_user(
    usuario_granja_id: int,
    conn=Depends(db_connection),
):
    delete_farm_user(conn, usuario_granja_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
