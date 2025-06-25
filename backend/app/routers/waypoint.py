from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import waypoint as schemas
from app.models import mission as models
from app.models.mission import Waypoint
from app.database import get_db

router = APIRouter(prefix="/waypoints", tags=["Waypoints"])

@router.post("/", response_model=schemas.Waypoint)
async def create_waypoint(wp: schemas.WaypointCreate, db: AsyncSession = Depends(get_db)):
    db_wp = wp_models.Waypoint(**wp.dict())
    db.add(db_wp)
    await db.commit()
    await db.refresh(db_wp)
    return db_wp

@router.get("/", response_model=list[schemas.Waypoint])
async def list_waypoints(db: AsyncSession = Depends(get_db)):
    result = await db.execute(wp_models.Waypoint.__table__.select())
    return result.scalars().all()
