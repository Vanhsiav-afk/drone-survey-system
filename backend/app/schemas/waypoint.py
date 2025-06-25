from pydantic import BaseModel
from typing import Optional

class WaypointBase(BaseModel):
    latitude: float
    longitude: float
    sequence: int
    mission_id: Optional[int]

class WaypointCreate(WaypointBase):
    pass

class Waypoint(WaypointBase):
    id: int

    class Config:
        orm_mode = True
