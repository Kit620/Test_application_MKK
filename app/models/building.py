"""Модель здания в справочнике."""

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class Building(Base):
    """Здание: адрес и географические координаты."""

    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    address = Column(String(512), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    organizations = relationship("Organization", back_populates="building")
