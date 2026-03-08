"""Модель вида деятельности (древовидная структура, до 3 уровней)."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class Activity(Base):
    """Вид деятельности; может иметь родителя (дерево до 3 уровней)."""

    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(256), nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True, index=True)
    level = Column(Integer, nullable=False)

    parent = relationship("Activity", remote_side=[id], backref="children")
    organizations = relationship(
        "Organization",
        secondary="organization_activities",
        back_populates="activities",
    )
