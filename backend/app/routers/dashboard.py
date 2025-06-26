from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import drone as drone_models, mission as mission_models
from app.schemas.dashboard import DashboardSummaryResponse, DroneStatusResponse, MissionProgressResponse
import datetime

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary(db: Session = Depends(get_db)):
    drones = db.query(drone_models.Drone).all()
    missions = db.query(mission_models.Mission).all()

    drone_responses = []
    for d in drones:
        drone_responses.append(DroneStatusResponse(
            id=d.id,
            name=d.name,
            status="in_mission" if d.current_mission_id else "available",
            battery_level=d.battery_level,
            current_mission_id=d.current_mission_id
        ))

    mission_responses = []
    for m in missions:
        total_waypoints = len(m.waypoints)
        if total_waypoints == 0:
            percent = 0
            remaining = None
        elif m.status in ["in_progress", "paused"]:
            now = datetime.datetime.utcnow()
            started_at = m.started_at or now
            elapsed = (now - started_at).total_seconds()
            completed = int(elapsed // 10)
            completed = min(completed, total_waypoints)
            percent = int((completed / total_waypoints) * 100)
            remaining = (total_waypoints - completed) * 10
        else:
            percent = 100 if m.status == "completed" else 0
            remaining = None

        mission_responses.append(MissionProgressResponse(
            id=m.id,
            name=m.name,
            status=m.status,
            percent_complete=percent,
            estimated_time_remaining_sec=remaining
        ))

    return DashboardSummaryResponse(
        drones=drone_responses,
        missions=mission_responses
    )
