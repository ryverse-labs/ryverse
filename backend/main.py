"""
Application entry point.
Registers routers and creates FastAPI app.
"""

from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.auth import router as auth_router

app = FastAPI(title="RyVerse API")

app.include_router(health_router)
app.include_router(auth_router)