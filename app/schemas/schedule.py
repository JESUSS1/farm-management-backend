from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel
from datetime import time, datetime


class ScheduleResponse(BaseModel):
    id: int
    nombre: str
    hora: time
    funcion: str
    target: str | None
    activo: bool
    ultima_ejecucion: datetime | None
    created_at: datetime | None
    updated_at: datetime | None

class ScheduleCreate(BaseModel):
    nombre: str
    hora: str
    funcion: str
    target: str
    activo: bool = True


class ScheduleUpdate(BaseModel):
    nombre: Optional[str] = None
    hora: Optional[str] = None
    funcion: Optional[str] = None
    target: Optional[str] = None
    activo: Optional[bool] = None