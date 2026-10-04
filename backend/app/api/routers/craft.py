from fastapi import APIRouter, Depends
from app.services.state_engine import state_engine
from app.services.ml_predictor import ml_service
from app.api.deps import require_permission

router = APIRouter(prefix="/craft", tags=["Craft Operations"])

@router.get("/summary")
def get_craft_summary(user: dict = Depends(require_permission("craft:read"))):
    fleet = state_engine.data["aircraft"]
    ready = sum(1 for a in fleet if a["status"] == "READY")
    maint = sum(1 for a in fleet if a["status"] == "MAINTENANCE")
    return {
        "fleet_total": len(fleet),
        "fleet_ready": ready,
        "fleet_in_maintenance": maint,
        "average_readiness_pct": 91.4,
        "average_component_health": 88.6,
        "predicted_constraints_2h": 4
    }

@router.get("/fleet")
def get_fleet(user: dict = Depends(require_permission("craft:read"))):
    return state_engine.data["aircraft"]

@router.get("/maintenance")
def get_maintenance(user: dict = Depends(require_permission("craft:read"))):
    return [
        {"aircraft_code": "A14", "task": "Turbine Core 100-Hr Inspection", "scheduled": "2026-10-05T14:00:00Z", "status": "OVERDUE"},
        {"aircraft_code": "A22", "task": "Radar Array Calibration", "scheduled": "2026-10-05T16:30:00Z", "status": "UPCOMING"}
    ]

@router.get("/predictions")
def get_predictions(user: dict = Depends(require_permission("craft:read"))):
    return ml_service.get_maintenance_predictions()
