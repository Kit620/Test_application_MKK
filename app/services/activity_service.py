"""Сервис видов деятельности: дерево для отображения."""

from typing import List

from sqlalchemy.orm import Session

from app.models import Activity
from app.schemas.activity import ActivityTreeSchema


def get_activities_tree(db: Session) -> List[ActivityTreeSchema]:
    """Все виды деятельности в виде дерева (корневые узлы с вложенными children)."""
    all_activities = db.query(Activity).order_by(Activity.level, Activity.id).all()
    by_id = {a.id: ActivityTreeSchema(id=a.id, name=a.name, level=a.level, children=[]) for a in all_activities}
    roots: List[ActivityTreeSchema] = []
    for a in all_activities:
        node = by_id[a.id]
        if a.parent_id is None:
            roots.append(node)
        else:
            parent = by_id.get(a.parent_id)
            if parent:
                parent.children.append(node)
    return roots
