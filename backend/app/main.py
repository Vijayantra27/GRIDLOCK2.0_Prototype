from fastapi import FastAPI

from app.routes.hotspots import router as hotspots_router
from app.routes.patrol import router as patrol_router
from app.routes.congestion import router as congestion_router
from app.routes.predictions import router as predictions_router
from app.routes.simulation import router as simulation_router
from app.routes.ai_assistant import router as assistant_router

app = FastAPI(
    title="GridLock AI",
    version="1.0.0"
)

app.include_router(
    hotspots_router
)

app.include_router(
    patrol_router
)

app.include_router(
    congestion_router
)

app.include_router(
    predictions_router
)

app.include_router(
    simulation_router
)

app.include_router(
    assistant_router
)


@app.get("/")
def root():

    return {
        "message": "GridLock AI Running"
    }