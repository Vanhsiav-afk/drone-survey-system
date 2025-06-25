from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db_base import Base

class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    altitude = Column(Float, default=50.0)
    overlap_percentage = Column(Float, default=30.0)

    waypoints = relationship("Waypoint", back_populates="mission", cascade="all, delete-orphan")


class Waypoint(Base):
    __tablename__ = "waypoints"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    sequence = Column(Integer, nullable=False)

    mission_id = Column(Integer, ForeignKey("missions.id"))
    mission = relationship("Mission", back_populates="waypoints")
