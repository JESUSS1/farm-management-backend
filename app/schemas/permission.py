from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PermissionBase(BaseModel):
    codigo: str = Field(
        min_length=1,
        max_length=100,
    )
    nombre: str = Field(
        min_length=1,
        max_length=100,
    )
    descripcion: Optional[str] = None


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    codigo: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    nombre: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    descripcion: Optional[str] = None
    estado: Optional[bool] = None


class PermissionResponse(PermissionBase):
    permiso_id: int
    estado: bool

    model_config = ConfigDict(
        from_attributes=True,
    )
