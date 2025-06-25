from pydantic import BaseModel
from typing import Optional

class MissionBase(BaseModel):
    name: str
    description: Optional[str] = None
    altitude: Optional[float] = None
    overlap_percentage: Optional[float] = None

class MissionCreate(MissionBase):
    pass

class Mission(MissionBase):
    id: int

    class Config:
        orm_mode = True
