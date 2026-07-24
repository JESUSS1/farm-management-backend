from fastapi import (
    APIRouter,
    Depends,
    Query,
    Response,
    status,
)

from app.core.auth import get_current_user, require_permissions
from app.core.database import db_connection
from app.schemas.farm import (
    FarmCreate,
    FarmResponse,
    FarmUpdate,
)
from app.services.farms_service import (
    create_farm,
    delete_farm,
    get_farm_by_id,
    list_farms,
    update_farm,
)

router = APIRouter(
    prefix="/farms",
    tags=["Farms"],
    dependencies=[
        Depends(get_current_user),
    ],
)


@router.get(
    "/",
    response_model=list[FarmResponse],
)
def get_farms(
    current_user: dict = Depends(require_permissions("FARMS_VIEW")),
    conn=Depends(db_connection),
    search: str | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return list_farms(
        conn,
        search=search,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{granja_id}",
    response_model=FarmResponse,
)
def get_farm(
    granja_id: int,
    current_user: dict = Depends(require_permissions("FARMS_VIEW")),
    conn=Depends(db_connection),
):
    return get_farm_by_id(conn, granja_id)


@router.post(
    "/",
    response_model=FarmResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_farm(
    farm_data: FarmCreate,
    current_user: dict = Depends(require_permissions("FARMS_CREATE")),
    conn=Depends(db_connection),
):
    return create_farm(conn, farm_data)


@router.patch(
    "/{granja_id}",
    response_model=FarmResponse,
)
def update_existing_farm(
    granja_id: int,
    farm_data: FarmUpdate,
    current_user: dict = Depends(require_permissions("FARMS_UPDATE")),
    conn=Depends(db_connection),
):
    return update_farm(conn, granja_id, farm_data)


@router.delete(
    "/{granja_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_farm(
    granja_id: int,
    current_user: dict = Depends(require_permissions("FARMS_DELETE")),
    conn=Depends(db_connection),
):
    delete_farm(conn, granja_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
