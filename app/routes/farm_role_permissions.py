from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from app.core.auth import get_current_user, require_permissions
from app.core.database import db_connection
from app.schemas.farm_role_permission import (
    FarmRolePermissionCreate,
    FarmRolePermissionUpdate,
    FarmRolePermissionResponse,
)
from app.services.farm_role_permissions_service import (
    create_farm_role_permission,
    delete_farm_role_permission,
    get_farm_role_permission_by_id,
    list_farm_role_permissions,
    update_farm_role_permission,
)

router = APIRouter(
    prefix="/farm-role-permissions",
    tags=["FarmRolePermissions"],
    dependencies=[
        Depends(get_current_user),
    ],
)


@router.get(
    "/",
    response_model=list[FarmRolePermissionResponse],
)
def get_farm_role_permissions(
    current_user: dict = Depends(require_permissions("PERMISSIONS_VIEW")),
    conn=Depends(db_connection),
):
    return list_farm_role_permissions(conn)


@router.get(
    "/{farm_role_permission_id}",
    response_model=FarmRolePermissionResponse,
)
def get_farm_role_permission(
    farm_role_permission_id: int,
    current_user: dict = Depends(require_permissions("PERMISSIONS_VIEW")),
    conn=Depends(db_connection),
):
    return get_farm_role_permission_by_id(conn, farm_role_permission_id)


@router.post(
    "/",
    response_model=FarmRolePermissionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_farm_role_permission(
    permission_data: FarmRolePermissionCreate,
    current_user: dict = Depends(require_permissions("PERMISSIONS_CREATE")),
    conn=Depends(db_connection),
):
    return create_farm_role_permission(conn, permission_data)


@router.patch(
    "/{farm_role_permission_id}",
    response_model=FarmRolePermissionResponse,
)
def update_existing_farm_role_permission(
    farm_role_permission_id: int,
    permission_data: FarmRolePermissionUpdate,
    current_user: dict = Depends(require_permissions("PERMISSIONS_UPDATE")),
    conn=Depends(db_connection),
):
    return update_farm_role_permission(
        conn,
        farm_role_permission_id,
        permission_data,
    )


@router.delete(
    "/{farm_role_permission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_farm_role_permission(
    farm_role_permission_id: int,
    current_user: dict = Depends(require_permissions("PERMISSIONS_DELETE")),
    conn=Depends(db_connection),
):
    delete_farm_role_permission(conn, farm_role_permission_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
