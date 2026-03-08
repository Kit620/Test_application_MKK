"""Pydantic-схемы для зданий."""

from pydantic import BaseModel, ConfigDict


class BuildingSchema(BaseModel):
    """Здание: адрес и координаты."""

    id: int
    address: str
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)
