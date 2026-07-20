from fastapi import (
    APIRouter,
    Depends,
    status,
)

from app.core.auth import (
    get_current_user,
)
from app.core.database import (
    db_connection,
)
from app.schemas.permission import (
    PermissionCreate,
    PermissionResponse,
)
from app.services.permissions_service import (
    create_permission,
    get_permission,
    list_permissions,
)

router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"],
    dependencies=[
        Depends(get_current_user),
    ],
)


@router.get(
    "/",
    response_model=list[PermissionResponse],
)
def get_all_permissions(
    conn=Depends(db_connection),
):
    return list_permissions(conn)


@router.get(
    "/{permiso_id}",
    response_model=PermissionResponse,
)
def get_permission_by_id(
    permiso_id: int,
    conn=Depends(db_connection),
):
    return get_permission(
        conn,
        permiso_id,
    )


@router.post(
    "/",
    response_model=PermissionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_permission(
    permission_data: PermissionCreate,
    conn=Depends(db_connection),
):
    return create_permission(
        conn,
        permission_data,
    )
