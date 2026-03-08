"""Сервис зданий: логика и доступ к БД."""

from typing import List

from sqlalchemy.orm import Session

from app.models import Building


def get_all_buildings(db: Session) -> List[Building]:
    """Список всех зданий."""
    return db.query(Building).order_by(Building.id).all()
