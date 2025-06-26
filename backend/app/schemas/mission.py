from enum import Enum
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MissionStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    paused = "paused"
    completed = "completed"
    aborted = "aborted"

class MissionBase(BaseModel):
    name: str
    description: Optional[str] = None
    altitude: Optional[float] = None
    overlap_percentage: Optional[float] = None

class MissionCreate(MissionBase):
    pass

class Mission(MissionBase):
    id: int
    status: MissionStatus

    class Config:
        orm_mode = True

class MissionSummaryResponse(BaseModel):
    mission_id: int
    name: str
    status: MissionStatus
    waypoints: int
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    duration_seconds: Optional[float]

    class Config:
        orm_mode = True

class OrgSurveyStatsResponse(BaseModel):
    total_missions: int
    completed: int
    aborted: int