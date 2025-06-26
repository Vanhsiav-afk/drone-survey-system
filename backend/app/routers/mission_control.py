from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import mission as models
from app.schemas.mission import MissionStatus

router = APIRouter(prefix="/mission-control", tags=["Mission Control"])

def get_mission_or_404(mission_id: int, db: Session) -> models.Mission:
    mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission

@router.post("/{mission_id}/start")
def start_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = get_mission_or_404(mission_id, db)
    if mission.status not in [MissionStatus.pending, MissionStatus.paused]:
        raise HTTPException(status_code=400, detail="Cannot start mission from current status")
    mission.status = MissionStatus.in_progress
    db.commit()
    return {"message": "Mission started"}

@router.post("/{mission_id}/pause")
def pause_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = get_mission_or_404(mission_id, db)
    if mission.status != MissionStatus.in_progress:
        raise HTTPException(status_code=400, detail="Only in-progress missions can be paused")
    mission.status = MissionStatus.paused
    db.commit()
    return {"message": "Mission paused"}

@router.post("/{mission_id}/resume")
def resume_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = get_mission_or_404(mission_id, db)
    if mission.status != MissionStatus.paused:
        raise HTTPException(status_code=400, detail="Only paused missions can be resumed")
    mission.status = MissionStatus.in_progress
    db.commit()
    return {"message": "Mission resumed"}

@router.post("/{mission_id}/abort")
def abort_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = get_mission_or_404(mission_id, db)
    if mission.status in [MissionStatus.completed, MissionStatus.aborted]:
        raise HTTPException(status_code=400, detail="Mission is already completed or aborted")
    mission.status = MissionStatus.aborted
    db.commit()
    return {"message": "Mission aborted"}
