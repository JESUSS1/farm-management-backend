from fastapi import FastAPI
from app.routes import health, readings, schedules
from app.version import __version__

app = FastAPI(
    title="Farm Management Backend",
    version=__version__,
)

app.include_router(health.router)
app.include_router(readings.router)
app.include_router(schedules.router)