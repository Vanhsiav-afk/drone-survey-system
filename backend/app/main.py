from fastapi import FastAPI
from app.routers import drone

app = FastAPI()

app.include_router(drone.router, prefix="/drones", tags=["Drones"])

@app.get("/")
def root():
    return {"message": "Drone Survey Backend is live!"}
