from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FarmCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    ubicacion: str | None = None
    descripcion: str | None = None


class FarmUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    ubicacion: str | None = None
    descripcion: str | None = None
    estado: bool | None = None

    @model_validator(mode="after")
    def validate_update_fields(self):
        if not self.model_fields_set:
            raise ValueError("Debe enviar al menos un campo para actualizar")

        return self


class FarmResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    granja_id: int
    nombre: str
    ubicacion: str | None
    descripcion: str | None
    estado: bool
    created_at: datetime
    updated_at: datetime
