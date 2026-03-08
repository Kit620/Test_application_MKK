"""Точка входа REST API справочника организаций."""

from fastapi import FastAPI

from app.api.routes import activities, buildings, organizations
from app.config import settings

app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url=None,
)

app.include_router(organizations.router)
app.include_router(buildings.router)
app.include_router(activities.router)


@app.get("/health")
def health():
    """Проверка доступности сервиса."""
    return {"status": "Привет"}
