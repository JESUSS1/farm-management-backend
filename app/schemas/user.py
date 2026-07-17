from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator,
)


class UserCreate(BaseModel):
    rol_sistema_id: int = Field(gt=0)

    username: str = Field(
        min_length=3,
        max_length=50,
    )

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    email: EmailStr | None = None

    nombres: str = Field(
        min_length=1,
        max_length=100,
    )

    apellidos: str = Field(
        min_length=1,
        max_length=100,
    )

    telefono: str | None = Field(
        default=None,
        max_length=30,
    )

    documento_identidad: str | None = Field(
        default=None,
        max_length=20,
    )


class UserUpdate(BaseModel):
    rol_sistema_id: int | None = Field(
        default=None,
        gt=0,
    )

    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=50,
    )

    email: EmailStr | None = None

    nombres: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    apellidos: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    telefono: str | None = Field(
        default=None,
        max_length=30,
    )

    documento_identidad: str | None = Field(
        default=None,
        max_length=20,
    )

    estado: bool | None = None

    @model_validator(mode="after")
    def validate_update_fields(self):
        if not self.model_fields_set:
            raise ValueError(
                "Debe enviar al menos un campo para actualizar"
            )

        return self


class UserPasswordUpdate(BaseModel):
    password: str = Field(
        min_length=8,
        max_length=128,
    )


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    usuario_id: int
    rol_sistema_id: int
    rol_sistema: str

    username: str
    email: str | None

    estado: bool

    persona_id: int
    nombres: str
    apellidos: str
    telefono: str | None
    documento_identidad: str | None

    created_at: datetime
    updated_at: datetime