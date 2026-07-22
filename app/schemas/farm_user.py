from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FarmUserCreate(BaseModel):
    usuario_id: int = Field(gt=0)
    granja_id: int = Field(gt=0)
    rol_granja_id: int = Field(gt=0)
    es_propietario: bool = False


class FarmUserUpdate(BaseModel):
    rol_granja_id: int | None = Field(default=None, gt=0)
    es_propietario: bool | None = None
    estado: bool | None = None

    @model_validator(mode="after")
    def validate_update_fields(self):
        if not self.model_fields_set:
            raise ValueError("Debe enviar al menos un campo para actualizar")

        return self


class FarmUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    usuario_granja_id: int
    usuario_id: int
    granja_id: int
    rol_granja_id: int
    es_propietario: bool
    estado: bool
    created_at: datetime
    updated_at: datetime
