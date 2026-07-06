from datetime import datetime
from pydantic import BaseModel


class ReadingResponse(BaseModel):
    id: int
    fecha: datetime
    device_id: str | None
    sensor: str | None
    variable: str | None
    valor: float | None
    unidad: str | None
    firmware_version: str | None