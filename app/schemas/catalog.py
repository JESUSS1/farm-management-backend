from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class CatalogBase(BaseModel):
    nombre: str = Field(
        min_length=1,
        max_length=100,
    )
    descripcion: Optional[str] = None
    estado: bool


class SystemRoleResponse(CatalogBase):
    rol_sistema_id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class PermissionCatalogResponse(CatalogBase):
    permiso_id: int
    codigo: str = Field(
        min_length=1,
        max_length=100,
    )

    model_config = ConfigDict(
        from_attributes=True,
    )
