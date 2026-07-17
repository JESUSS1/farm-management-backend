from fastapi import FastAPI
from app.routes import health, readings, schedules, users
from app.version import __version__

app = FastAPI(
    title="Farm Management Backend",
    version=__version__,
)
app.include_router(users.router)
app.include_router(health.router)
app.include_router(readings.router)
app.include_router(schedules.router)
