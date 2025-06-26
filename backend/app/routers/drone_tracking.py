from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.database import get_db
from app.models.drone import Drone
from fastapi import BackgroundTasks
from app.utils.simulate_movement import simulate_drone_movement
router = APIRouter(prefix="/tracking", tags=["Drone Tracking"])

class LocationUpdateRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

@router.post("/drones/{drone_id}/update-location")
def update_location(drone_id: int, req: LocationUpdateRequest, db: Session = Depends(get_db)):
    drone = db.query(Drone).filter(Drone.id == drone_id).first()
    if not drone:
        raise HTTPException(status_code=404, detail="Drone not found")

    drone.latitude = req.latitude
    drone.longitude = req.longitude
    db.commit()

    return {"message": "Location updated successfully"}
@router.get("/drones/{drone_id}/location")
def get_location(drone_id: int, db: Session = Depends(get_db)):
    drone = db.query(Drone).filter(Drone.id == drone_id).first()
    if not drone:
        raise HTTPException(status_code=404, detail="Drone not found")

    return {
        "drone_id": drone.id,
        "latitude": drone.latitude,
        "longitude": drone.longitude
    }


@router.post("/drones/{drone_id}/simulate")
def simulate(drone_id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(simulate_drone_movement, drone_id)
    return {"message": f"Simulation started for drone {drone_id}"}
