from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db_base import Base
import enum


class DroneStatus(str, enum.Enum):
    idle = "idle"
    in_mission = "in_mission"
    charging = "charging"


class Drone(Base):
    __tablename__ = "drones"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, nullable=False)
    battery_level = Column(Float, nullable=False)
    status = Column(Enum(DroneStatus), default=DroneStatus.idle)

    current_mission_id = Column(Integer, ForeignKey("missions.id"), nullable=True)
    current_mission = relationship("Mission", back_populates="assigned_drones")
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
