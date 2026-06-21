from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.hotspots import router as hotspots_router
from app.routes.patrol import router as patrol_router
from app.routes.congestion import router as congestion_router
from app.routes.predictions import router as predictions_router
from app.routes.simulation import router as simulation_router
from app.routes.ai_assistant import router as assistant_router
from app.routes.officers import router as officers_router
from app.routes.dna import router as dna_router
from app.routes.propagation import router as propagation_router
from app.routes.dashboard import router as dashboard_router
from app.routes.risk import router as risk_router
from app.routes.assistant import router as assistant_router
from app.routes.routes import router as routes_router
from app.routes.emerging import router as emerging_router
from app.routes.dashboard import router as dashboard_router
from app.routes.report import router as report_router
from app.routes.optimizer import router as optimizer_router
from app.routes.recommend import router as recommend_router
from app.routes.officer_recommendation import router as officer_router
from app.routes.impact import router as impact_router
from app.routes.advisor import router as advisor_router
from app.routes.coverage import router as coverage_router
app = FastAPI(
    title="GridLock AI",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


app.include_router(officers_router)
app.include_router(dna_router)
app.include_router(propagation_router)
app.include_router(dashboard_router)
app.include_router(risk_router)
app.include_router(assistant_router)
app.include_router(routes_router)
app.include_router(emerging_router)
app.include_router(dashboard_router)
app.include_router(report_router)

app.include_router(
    optimizer_router
)
app.include_router(
    recommend_router
)

app.include_router(
    officer_router
)

app.include_router(
    impact_router
)
app.include_router(
    advisor_router
)

app.include_router(
    coverage_router
)

@app.get("/")
def root():

    return {
        "message": "GridLock AI Running"
    }