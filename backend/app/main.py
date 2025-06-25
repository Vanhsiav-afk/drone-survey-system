from fastapi import FastAPI
from app.routers import drone, mission, waypoint

app = FastAPI(title="Drone Survey System")

app.include_router(drone.router)
app.include_router(mission.router)
app.include_router(waypoint.router)
