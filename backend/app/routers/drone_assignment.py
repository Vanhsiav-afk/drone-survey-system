from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import drone as drone_models, mission as mission_models
from pydantic import BaseModel

router = APIRouter(prefix="/missions", tags=["Drone Assignment"])

class AssignDroneRequest(BaseModel):
    drone_id: int

@router.post("/{mission_id}/assign-drone")
def assign_drone_to_mission(mission_id: int, request: AssignDroneRequest, db: Session = Depends(get_db)):
    drone = db.query(drone_models.Drone).filter(drone_models.Drone.id == request.drone_id).first()
    if not drone:
        raise HTTPException(status_code=404, detail="Drone not found")

    mission = db.query(mission_models.Mission).filter(mission_models.Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    if drone.current_mission_id is not None:
        raise HTTPException(status_code=400, detail="Drone is already assigned to a mission")

    # Assign drone to mission
    drone.current_mission = mission
    drone.status = drone_models.DroneStatus.in_mission
    db.commit()

    return {"message": f"Drone {drone.id} assigned to mission {mission.id}"}
