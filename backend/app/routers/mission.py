from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import mission as schemas
from app.models import mission as models
from app.database import get_db

router = APIRouter(prefix="/missions", tags=["Missions"])

@router.post("/", response_model=schemas.Mission)
async def create_mission(mission: schemas.MissionCreate, db: AsyncSession = Depends(get_db)):
    db_mission = models.Mission(**mission.dict())
    db.add(db_mission)
    await db.commit()
    await db.refresh(db_mission)
    return db_mission

@router.get("/", response_model=list[schemas.Mission])
async def list_missions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(models.Mission.__table__.select())
    return result.scalars().all()
