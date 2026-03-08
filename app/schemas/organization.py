"""Pydantic-схемы для организаций."""

from typing import List

from pydantic import BaseModel, ConfigDict


class PhoneSchema(BaseModel):
    """Номер телефона организации."""

    id: int
    phone_number: str

    model_config = ConfigDict(from_attributes=True)


class ActivityBriefSchema(BaseModel):
    """Краткое описание вида деятельности."""

    id: int
    name: str
    level: int

    model_config = ConfigDict(from_attributes=True)


class BuildingBriefSchema(BaseModel):
    """Краткое описание здания."""

    id: int
    address: str
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)


class OrganizationSchema(BaseModel):
    """Полная карточка организации."""

    id: int
    name: str
    building: BuildingBriefSchema
    phones: List[PhoneSchema]
    activities: List[ActivityBriefSchema]

    model_config = ConfigDict(from_attributes=True)


class OrganizationListSchema(BaseModel):
    """Организация в списке (без глубокой вложенности при необходимости)."""

    id: int
    name: str
    building: BuildingBriefSchema
    phones: List[PhoneSchema]
    activities: List[ActivityBriefSchema]

    model_config = ConfigDict(from_attributes=True)
