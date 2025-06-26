import asyncio
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.drone import Drone
from app.models.mission import Mission

async def simulate_drone_movement(drone_id: int):
    async with AsyncSessionLocal() as db:
        # Get the drone
        result = await db.execute(select(Drone).filter(Drone.id == drone_id))
        drone = result.scalar_one_or_none()

        if not drone or not drone.current_mission:
            return

        waypoints = drone.current_mission.waypoints
        if not waypoints:
            return

        for wp in waypoints:
            drone.latitude = wp.latitude
            drone.longitude = wp.longitude
            await db.commit()

            print(f"[SIMULATION] Drone {drone_id} moved to ({wp.latitude}, {wp.longitude})")
            await asyncio.sleep(5)  # simulate 5 sec per waypoint
