"""Сервис организаций: логика и доступ к БД."""

import math
from typing import List, Optional, Set

from sqlalchemy.orm import Session, joinedload

from app.models import Activity, Building, Organization

EARTH_RADIUS_KM = 6371.0
KM_PER_DEGREE_APPROX = 111.0

_org_load = (
    joinedload(Organization.building),
    joinedload(Organization.phones),
    joinedload(Organization.activities),
)


def get_organization(organization_id: int, db: Session) -> Optional[Organization]:
    """Организация по id или None."""
    return (
        db.query(Organization)
        .options(*_org_load)
        .filter(Organization.id == organization_id)
        .first()
    )


def get_organizations_by_building(building_id: int, db: Session) -> List[Organization]:
    """Организации в указанном здании."""
    return (
        db.query(Organization)
        .options(*_org_load)
        .filter(Organization.building_id == building_id)
        .order_by(Organization.name)
        .all()
    )


def _activity_ids_in_subtree(db: Session, activity_id: int) -> List[int]:
    """Id деятельности и всех потомков в дереве (до 3 уровней)."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        return []
    result: Set[int] = {activity_id}
    _collect_descendant_ids(db, activity_id, result)
    return list(result)


def _collect_descendant_ids(db: Session, parent_id: int, out: Set[int]) -> None:
    children = db.query(Activity).filter(Activity.parent_id == parent_id).all()
    for child in children:
        out.add(child.id)
        _collect_descendant_ids(db, child.id, out)


def get_organizations_by_activity(
    activity_id: int,
    db: Session,
    include_children: bool = True,
) -> List[Organization]:
    """
    Организации по виду деятельности.
    При include_children=True — включая все вложенные в дереве (Еда → Мясная, Молочная и т.д.).
    """
    if include_children:
        activity_ids = _activity_ids_in_subtree(db, activity_id)
    else:
        a = db.query(Activity).filter(Activity.id == activity_id).first()
        activity_ids = [a.id] if a else []
    if not activity_ids:
        return []
    return (
        db.query(Organization)
        .options(*_org_load)
        .join(Organization.activities)
        .filter(Activity.id.in_(activity_ids))
        .distinct()
        .order_by(Organization.name)
        .all()
    )


def get_organizations_in_bbox(
    min_latitude: float,
    max_latitude: float,
    min_longitude: float,
    max_longitude: float,
    db: Session,
) -> List[Organization]:
    """Организации, чьи здания в заданной прямоугольной области."""
    return (
        db.query(Organization)
        .options(*_org_load)
        .join(Building)
        .filter(
            Building.latitude >= min_latitude,
            Building.latitude <= max_latitude,
            Building.longitude >= min_longitude,
            Building.longitude <= max_longitude,
        )
        .order_by(Organization.name)
        .all()
    )


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Расстояние между двумя точками в км (формула Haversine)."""
    lat1_r = math.radians(lat1)
    lat2_r = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2
    return EARTH_RADIUS_KM * 2 * math.asin(math.sqrt(a))


def get_organizations_in_radius(
    latitude: float,
    longitude: float,
    radius_km: float,
    db: Session,
) -> List[Organization]:
    """Организации, чьи здания в радиусе radius_km от точки."""
    delta = radius_km / KM_PER_DEGREE_APPROX
    cos_lat = max(0.1, abs(math.cos(math.radians(latitude))))
    min_lat, max_lat = latitude - delta, latitude + delta
    min_lon = longitude - delta / cos_lat
    max_lon = longitude + delta / cos_lat
    candidates = get_organizations_in_bbox(min_lat, max_lat, min_lon, max_lon, db)
    return [
        org
        for org in candidates
        if _haversine_km(latitude, longitude, org.building.latitude, org.building.longitude) <= radius_km
    ]


def search_organizations_by_name(name: str, db: Session) -> List[Organization]:
    """Поиск организаций по подстроке в названии."""
    if not name or not name.strip():
        return []
    pattern = f"%{name.strip()}%"
    return (
        db.query(Organization)
        .options(*_org_load)
        .filter(Organization.name.ilike(pattern))
        .order_by(Organization.name)
        .all()
    )
