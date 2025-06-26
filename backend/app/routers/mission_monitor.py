from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import mission as models
import datetime

router = APIRouter(prefix="/mission-monitor", tags=["Mission Monitoring"])

def get_mission_or_404(mission_id: int, db: Session) -> models.Mission:
    mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission

@router.get("/{mission_id}/progress")
def get_mission_progress(mission_id: int, db: Session = Depends(get_db)):
    mission = get_mission_or_404(mission_id, db)

    total_waypoints = len(mission.waypoints)
    if total_waypoints == 0:
        return {
            "status": mission.status,
            "percent_complete": 0,
            "estimated_time_remaining_sec": None
        }

    if mission.status not in ["in_progress", "paused"]:
        return {
            "status": mission.status,
            "percent_complete": 0,
            "estimated_time_remaining_sec": None
        }

    now = datetime.datetime.utcnow()
    started_at = mission.started_at or now
    elapsed_seconds = (now - started_at).total_seconds()

    waypoints_completed = int(elapsed_seconds // 10)
    waypoints_completed = min(waypoints_completed, total_waypoints)

    percent_complete = int((waypoints_completed / total_waypoints) * 100)
    estimated_time_remaining = (total_waypoints - waypoints_completed) * 10

    return {
        "status": mission.status,
        "percent_complete": percent_complete,
        "estimated_time_remaining_sec": estimated_time_remaining
    }
