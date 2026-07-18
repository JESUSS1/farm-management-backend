from fastapi import FastAPI
from app.routes import health, readings, schedules, users
from app.version import __version__
from app.core.handlers import register_exception_handlers
from app.routes import auth

app = FastAPI(
    title="Farm Management Backend",
    version=__version__,
)
register_exception_handlers(app)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(health.router)
app.include_router(readings.router)
app.include_router(schedules.router)
