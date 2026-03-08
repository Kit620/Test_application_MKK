"""Модели организации, телефонов и связки с видами деятельности."""

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.db import Base

organization_activities = Table(
    "organization_activities",
    Base.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True),
    Column("activity_id", Integer, ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True),
)


class Organization(Base):
    """Организация: название, одно здание, несколько телефонов и видов деятельности."""

    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(512), nullable=False, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id", ondelete="RESTRICT"), nullable=False, index=True)

    building = relationship("Building", back_populates="organizations")
    phones = relationship("OrganizationPhone", back_populates="organization", cascade="all, delete-orphan")
    activities = relationship(
        "Activity",
        secondary=organization_activities,
        back_populates="organizations",
    )


class OrganizationPhone(Base):
    """Номер телефона организации (у одной организации может быть несколько)."""

    __tablename__ = "organization_phones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    phone_number = Column(String(64), nullable=False)

    organization = relationship("Organization", back_populates="phones")
