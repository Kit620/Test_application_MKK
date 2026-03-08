"""Эндпоинты: список зданий."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_api_key
from app.db import get_db
from app.schemas.building import BuildingSchema
from app.services import building_service

router = APIRouter(prefix="/buildings", tags=["buildings"])


@router.get(
    "",
    response_model=List[BuildingSchema],
    summary="Список всех зданий",
)
def list_buildings(
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    buildings = building_service.get_all_buildings(db)
    return [BuildingSchema.model_validate(b) for b in buildings]
