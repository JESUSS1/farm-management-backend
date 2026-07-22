from fastapi import FastAPI
from app.routes import health, readings, schedules, users
from app.version import __version__
from app.core.handlers import register_exception_handlers
from app.routes import auth
from fastapi.middleware.cors import CORSMiddleware
from app.config import CORS_ORIGINS
from app.routes.permissions import (
    router as permissions_router,
)
from app.routes.catalogs import (
    router as catalogs_router,
)
from app.routes.farm_roles import (
    router as farm_roles_router,
)
from app.routes.farm_role_permissions import (
    router as farm_role_permissions_router,
)
from app.routes.farms import (
    router as farms_router,
)
from app.routes.farm_users import (
    router as farm_users_router,
)

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
# app.include_router(health.router)
# app.include_router(readings.router)
# app.include_router(schedules.router)
app.include_router(permissions_router)
app.include_router(catalogs_router)
app.include_router(farm_roles_router)
app.include_router(farm_role_permissions_router)
app.include_router(farms_router)
app.include_router(farm_users_router)
