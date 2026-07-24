from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FarmRoleCreate(BaseModel):
    granja_id: int = Field(gt=0)
    nombre: str = Field(min_length=1, max_length=80)
    descripcion: str | None = None


class FarmRoleCloneRequest(BaseModel):
    granja_id: int = Field(gt=0)
    nombre: str | None = Field(default=None, min_length=1, max_length=80)
    descripcion: str | None = None


class FarmRoleUpdate(BaseModel):
    granja_id: int | None = Field(default=None, gt=0)
    nombre: str | None = Field(default=None, min_length=1, max_length=80)
    descripcion: str | None = None
    estado: bool | None = None

    @model_validator(mode="after")
    def validate_update_fields(self):
        if not self.model_fields_set:
            raise ValueError("Debe enviar al menos un campo para actualizar")

        return self


class FarmRoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    rol_granja_id: int
    granja_id: int
    nombre: str
    descripcion: str | None
    estado: bool
    created_at: datetime
    updated_at: datetime
