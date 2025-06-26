from pydantic import BaseModel
from enum import Enum
from typing import Optional


class DroneStatus(str, Enum):
    idle = "idle"
    in_mission = "in_mission"
    charging = "charging"


class DroneCreate(BaseModel):
    model: str
    battery_level: float


class DroneOut(BaseModel):
    id: int
    model: str
    battery_level: float
    status: DroneStatus
    current_mission_id: Optional[int] = None

    class Config:
        orm_mode = True
