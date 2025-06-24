from sqlalchemy import Column, String, Float, Enum
from geoalchemy2 import Geography
from app.db_base import Base
import enum
import uuid

class DroneStatus(str, enum.Enum):
    idle = "idle"
    in_mission = "in_mission"
    charging = "charging"

class Drone(Base):
    __tablename__ = "drones"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    model = Column(String, nullable=False)
    battery_level = Column(Float, nullable=False)
    status = Column(Enum(DroneStatus), default=DroneStatus.idle)
    location = Column(Geography(geometry_type="POINT", srid=4326))
