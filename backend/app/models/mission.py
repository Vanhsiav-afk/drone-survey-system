from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.db_base import Base
from app.schemas.mission import MissionStatus  # ✅ Import the Enum from schemas
import datetime


class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    altitude = Column(Float, default=50.0)
    overlap_percentage = Column(Float, default=30.0)

    status = Column(Enum(MissionStatus), default=MissionStatus.pending, nullable=False)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)

    # Relationships
    waypoints = relationship("Waypoint", back_populates="mission", cascade="all, delete-orphan")
    assigned_drones = relationship("Drone", back_populates="current_mission", cascade="all, delete-orphan")
class Waypoint(Base):
    __tablename__ = "waypoints"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, nullable=True)

    mission_id = Column(Integer, ForeignKey("missions.id"))
    mission = relationship("Mission", back_populates="waypoints")