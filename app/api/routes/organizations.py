"""Эндпоинты: организации (по id, по зданию, по деятельности, по геозоне, поиск по названию)."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import require_api_key
from app.db import get_db
from app.schemas.organization import OrganizationListSchema, OrganizationSchema
from app.services import organization_service

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.get(
    "",
    response_model=List[OrganizationListSchema],
    summary="Список организаций с фильтрами",
    description=(
        "Один из параметров: building_id, activity_id, lat+lon+radius_km, "
        "bbox (min_lat, max_lat, min_lon, max_lon), name. "
        "При activity_id поиск идёт по виду деятельности и всем вложенным в дереве."
    ),
)
def list_organizations(
    building_id: Optional[int] = Query(None, description="Фильтр: организации в здании"),
    activity_id: Optional[int] = Query(None, description="Фильтр: вид деятельности (включая вложенные)"),
    latitude: Optional[float] = Query(None, description="Центр круга для поиска по радиусу"),
    longitude: Optional[float] = Query(None, description="Центр круга для поиска по радиусу"),
    radius_km: Optional[float] = Query(None, gt=0, description="Радиус в км"),
    min_lat: Optional[float] = Query(None, alias="min_lat", description="Прямоугольник: мин. широта"),
    max_lat: Optional[float] = Query(None, alias="max_lat", description="Прямоугольник: макс. широта"),
    min_lon: Optional[float] = Query(None, alias="min_lon", description="Прямоугольник: мин. долгота"),
    max_lon: Optional[float] = Query(None, alias="max_lon", description="Прямоугольник: макс. долгота"),
    name: Optional[str] = Query(None, description="Поиск по подстроке в названии"),
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    if building_id is not None:
        orgs = organization_service.get_organizations_by_building(building_id, db)
    elif activity_id is not None:
        orgs = organization_service.get_organizations_by_activity(activity_id, db, include_children=True)
    elif latitude is not None and longitude is not None and radius_km is not None:
        orgs = organization_service.get_organizations_in_radius(latitude, longitude, radius_km, db)
    elif min_lat is not None and max_lat is not None and min_lon is not None and max_lon is not None:
        orgs = organization_service.get_organizations_in_bbox(
            min_lat, max_lat, min_lon, max_lon, db
        )
    elif name is not None and name.strip():
        orgs = organization_service.search_organizations_by_name(name.strip(), db)
    else:
        raise HTTPException(
            status_code=422,
            detail="Укажите один из фильтров: building_id, activity_id, lat+lon+radius_km, bbox (min_lat, max_lat, min_lon, max_lon), name",
        )
    return [OrganizationListSchema.model_validate(o) for o in orgs]


@router.get(
    "/{organization_id}",
    response_model=OrganizationSchema,
    summary="Организация по id",
)
def get_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    org = organization_service.get_organization(organization_id, db)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return OrganizationSchema.model_validate(org)
