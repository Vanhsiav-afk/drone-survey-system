from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import drone as models
from app.schemas import drone as schemas

router = APIRouter()

@router.post("/", response_model=schemas.DroneOut)
async def create_drone(drone: schemas.DroneCreate, db: AsyncSession = Depends(get_db)):
    new_drone = models.Drone(
        model=drone.model,
        battery_level=drone.battery_level
    )
    db.add(new_drone)
    await db.commit()
    await db.refresh(new_drone)
    return new_drone

@router.get("/", response_model=list[schemas.DroneOut])
async def list_drones(db: AsyncSession = Depends(get_db)):
    result = await db.execute(models.Drone.__table__.select())
    return result.scalars().all()
