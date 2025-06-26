from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.database import get_db
from app.models import mission as models
from app.schemas.mission import MissionSummaryResponse, OrgSurveyStatsResponse, MissionStatus

router = APIRouter(prefix="/survey-report", tags=["Survey Reporting"])


@router.get("/summary/{mission_id}", response_model=MissionSummaryResponse)
def get_mission_summary(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()

    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    # Calculate duration if start and end exist
    if mission.started_at and mission.ended_at:
        duration = (mission.ended_at - mission.started_at).total_seconds()
    else:
        duration = None

    summary = MissionSummaryResponse(
        mission_id=mission.id,
        name=mission.name,
        status=mission.status,
        waypoints=len(mission.waypoints),
        started_at=mission.started_at,
        ended_at=mission.ended_at,
        duration_seconds=duration
    )
    return summary


@router.get("/org-stats", response_model=OrgSurveyStatsResponse)
def get_organization_stats(db: Session = Depends(get_db)):
    total = db.query(func.count(models.Mission.id)).scalar()
    completed = db.query(func.count(models.Mission.id)).filter(models.Mission.status == MissionStatus.completed).scalar()
    aborted = db.query(func.count(models.Mission.id)).filter(models.Mission.status == MissionStatus.aborted).scalar()

    return OrgSurveyStatsResponse(
        total_missions=total,
        completed=completed,
        aborted=aborted
    )
