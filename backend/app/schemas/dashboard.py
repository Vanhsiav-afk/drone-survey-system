from pydantic import BaseModel
from typing import Optional, List
from app.schemas.mission import MissionStatus

class DroneStatusResponse(BaseModel):
    id: int
    name: str
    status: str  # "available" or "in_mission"
    battery_level: float
    current_mission_id: Optional[int] = None

class MissionProgressResponse(BaseModel):
    id: int
    name: str
    status: MissionStatus
    percent_complete: int
    estimated_time_remaining_sec: Optional[int]

class DashboardSummaryResponse(BaseModel):
    drones: List[DroneStatusResponse]
    missions: List[MissionProgressResponse]
