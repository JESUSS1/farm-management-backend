from pydantic import BaseModel, ConfigDict, Field, model_validator


class FarmRolePermissionCreate(BaseModel):
    farm_role_id: int = Field(gt=0)
    permission_id: int = Field(gt=0)


class FarmRolePermissionUpdate(BaseModel):
    permission_id: int | None = Field(default=None, gt=0)
    estado: bool | None = None

    @model_validator(mode="after")
    def validate_update_fields(self):
        if not self.model_fields_set:
            raise ValueError("Debe enviar al menos un campo para actualizar")

        return self


class FarmRolePermissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    rol_granja_permiso_id: int
    rol_granja_id: int
    permission_id: int
    estado: bool
