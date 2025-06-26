from fastapi import FastAPI
from app.routers import drone, mission, waypoint, mission_control, mission_monitor,survey_report,dashboard,drone_assignment,drone_tracking

app = FastAPI(title="Drone Survey System")

app.include_router(drone.router)
app.include_router(mission.router)
app.include_router(waypoint.router)
app.include_router(mission_control.router)
app.include_router(mission_monitor.router)
app.include_router(survey_report.router)
app.include_router(dashboard.router)
app.include_router(drone_assignment.router)
app.include_router(drone_tracking.router)