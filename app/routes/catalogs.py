from fastapi import (
    APIRouter,
    Depends,
)

from app.core.auth import (
    get_current_user,
)
from app.core.database import (
    db_connection,
)
from app.schemas.catalog import (
    PermissionCatalogResponse,
    SystemRoleResponse,
)
from app.services.catalogs_service import (
    list_permissions,
    list_system_roles,
)

router = APIRouter(
    prefix="/catalogs",
    tags=["Catalogs"],
    dependencies=[
        Depends(get_current_user),
    ],
)


@router.get(
    "/system-roles",
    response_model=list[SystemRoleResponse],
)
def get_system_roles_catalog(
    conn=Depends(db_connection),
):
    return list_system_roles(conn)


@router.get(
    "/permissions",
    response_model=list[PermissionCatalogResponse],
)
def get_permissions_catalog(
    conn=Depends(db_connection),
):
    return list_permissions(conn)
