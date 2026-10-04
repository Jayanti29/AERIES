from fastapi import APIRouter, Depends
from app.services.state_engine import state_engine
from app.api.deps import require_permission

router = APIRouter(prefix="/supply", tags=["Supply Logistics"])

@router.get("/summary")
def get_supply_summary(user: dict = Depends(require_permission("supply:read"))):
    stocks = state_engine.data["resources"]
    critical = sum(1 for s in stocks if s["pressure_level"] == "CRITICAL")
    elevated = sum(1 for s in stocks if s["pressure_level"] == "ELEVATED")
    return {
        "resource_types_tracked": 12,
        "resources_under_pressure": critical + elevated,
        "projected_shortfalls_2h": critical,
        "average_reserve_margin_pct": 28.5,
        "bases_with_constraints": ["B-Delta", "B-Echo"]
    }

@router.get("/resources")
def get_resources(user: dict = Depends(require_permission("supply:read"))):
    return state_engine.data["resources"]

@router.get("/forecast/{resource_id}")
def get_resource_forecast(resource_id: str, user: dict = Depends(require_permission("supply:read"))):
    return {
        "resource_id": resource_id,
        "projections": [
            {"horizon": "+15m", "demand": 4300, "capacity": 5000, "confidence_band": [4100, 4500]},
            {"horizon": "+30m", "demand": 4650, "capacity": 5000, "confidence_band": [4400, 4850]},
            {"horizon": "+60m", "demand": 5100, "capacity": 5000, "confidence_band": [4800, 5350]},
            {"horizon": "+120m", "demand": 5700, "capacity": 5000, "confidence_band": [5300, 6100]}
        ],
        "threshold": 5000
    }
