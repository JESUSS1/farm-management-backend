from fastapi import FastAPI
from app.routes import health, readings, schedules, users
from app.version import __version__
from app.core.handlers import register_exception_handlers
from app.routes import auth
from fastapi.middleware.cors import CORSMiddleware
from app.config import CORS_ORIGINS

app = FastAPI(
    title="Farm Management Backend",
    version=__version__,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
register_exception_handlers(app)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(health.router)
app.include_router(readings.router)
app.include_router(schedules.router)
