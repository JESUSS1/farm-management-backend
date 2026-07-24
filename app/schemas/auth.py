from pydantic import BaseModel, Field


class FarmMembershipContext(BaseModel):
    usuario_granja_id: int
    granja_id: int
    granja_nombre: str
    rol_granja_id: int
    rol_granja_nombre: str
    es_propietario: bool
    estado: bool
    permissions: list[str] = Field(default_factory=list)


class LoginRequest(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
    )
    password: str = Field(
        min_length=8,
        max_length=128,
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AuthenticatedUserResponse(BaseModel):
    usuario_id: int
    username: str
    rol_sistema_id: int
    rol_nombre: str
    es_propietario: bool = False
    active_farm_id: int | None = None
    farm_memberships: list[FarmMembershipContext] = Field(default_factory=list)
    permissions: list[str] = Field(default_factory=list)
    estado: bool
