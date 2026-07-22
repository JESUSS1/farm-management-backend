from fastapi import (
    APIRouter,
    Depends,
    Query,
    Response,
    status,
)

from app.core.auth import get_current_user
from app.core.database import db_connection
from app.schemas.farm_role import (
    FarmRoleCreate,
    FarmRoleResponse,
    FarmRoleUpdate,
)
from app.services.farm_roles_service import (
    create_farm_role,
    delete_farm_role,
    get_farm_role_by_id,
    list_farm_roles,
    update_farm_role,
)

router = APIRouter(
    prefix="/farm-roles",
    tags=["FarmRoles"],
    dependencies=[
        Depends(get_current_user),
    ],
)


@router.get(
    "/",
    response_model=list[FarmRoleResponse],
)
def get_farm_roles(
    conn=Depends(db_connection),
    search: str | None = None,
    granja_id: int | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return list_farm_roles(
        conn,
        search=search,
        granja_id=granja_id,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{farm_role_id}",
    response_model=FarmRoleResponse,
)
def get_farm_role(
    farm_role_id: int,
    conn=Depends(db_connection),
):
    return get_farm_role_by_id(conn, farm_role_id)


@router.post(
    "/",
    response_model=FarmRoleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_farm_role(
    farm_role_data: FarmRoleCreate,
    conn=Depends(db_connection),
):
    return create_farm_role(conn, farm_role_data)


@router.patch(
    "/{farm_role_id}",
    response_model=FarmRoleResponse,
)
def update_existing_farm_role(
    farm_role_id: int,
    farm_role_data: FarmRoleUpdate,
    conn=Depends(db_connection),
):
    return update_farm_role(conn, farm_role_id, farm_role_data)


@router.delete(
    "/{farm_role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_farm_role(
    farm_role_id: int,
    conn=Depends(db_connection),
):
    delete_farm_role(conn, farm_role_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
