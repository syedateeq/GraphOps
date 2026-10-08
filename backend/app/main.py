"""
GraphOps FastAPI Application Entry Point.

Configures the FastAPI app, CORS, lifespan events, and routes.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import app_settings
from app.database import db
from app.routes.health import router as health_router
from app.routes.blast_radius import router as blast_radius_router
from app.routes.attack_path import router as attack_path_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Manage application startup and shutdown events."""
    # Startup
    print(f"Starting {app_settings.app_name} v{app_settings.app_version}")
    db.connect()
    yield
    # Shutdown
    db.close()
    print(f"{app_settings.app_name} shut down.")


app = FastAPI(
    title=app_settings.app_name,
    version=app_settings.app_version,
    description="Cybersecurity Graph Intelligence Platform",
    lifespan=lifespan,
)

# CORS — allow the Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(health_router)
app.include_router(blast_radius_router)
app.include_router(attack_path_router)
