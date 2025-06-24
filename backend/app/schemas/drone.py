from pydantic import BaseModel
from enum import Enum

class DroneStatus(str, Enum):
    idle = "idle"
    in_mission = "in_mission"
    charging = "charging"

class DroneCreate(BaseModel):
    model: str
    battery_level: float

class DroneOut(BaseModel):
    id: str
    model: str
    battery_level: float
    status: DroneStatus

    class Config:
        orm_mode = True
