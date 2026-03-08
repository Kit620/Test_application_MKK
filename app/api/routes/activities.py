"""Эндпоинты: дерево видов деятельности."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_api_key
from app.db import get_db
from app.schemas.activity import ActivityTreeSchema
from app.services import activity_service

router = APIRouter(prefix="/activities", tags=["activities"])


@router.get(
    "",
    response_model=List[ActivityTreeSchema],
    summary="Дерево видов деятельности",
)
def get_activities_tree(
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    """Список корневых видов деятельности с вложенными дочерними (до 3 уровней)."""
    return activity_service.get_activities_tree(db)
