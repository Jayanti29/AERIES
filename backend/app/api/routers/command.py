from fastapi import APIRouter, Depends
from app.services.state_engine import state_engine
from app.api.deps import require_permission

router = APIRouter(prefix="/command", tags=["Command Center"])

@router.get("/summary")
def get_summary(user: dict = Depends(require_permission("command:read"))):
    return state_engine.get_summary()

@router.get("/health")
def get_health(user: dict = Depends(require_permission("command:read"))):
    return state_engine.get_domain_health()

@router.get("/map-layers")
def get_map_layers(user: dict = Depends(require_permission("map:read"))):
    return {
        "bases": state_engine.data["bases"],
        "aircraft": state_engine.data["aircraft"][:20],
        "airspace_zones": [
            {"code": "Z-01", "name": "Northern Corridor Alpha", "status": "CLEAR", "min_alt_ft": 10000, "max_alt_ft": 45000},
            {"code": "Z-02", "name": "Desert Strike Sector 4", "status": "RESTRICTED", "reason": "High Turbulence & Crosswinds"}
        ]
    }

@router.get("/insights")
def get_insights(user: dict = Depends(require_permission("insights:read"))):
    return {
        "insights": [
            {
                "id": "INS-01",
                "category": "HIDDEN_CONSTRAINT",
                "title": "B-Delta Fuel Reserve Exhaustion Risk",
                "severity": "CRITICAL",
                "confidence": 0.94,
                "description": "Jet Fuel draw rate at B-Delta exceeds inbound replenishment schedule by 22% under current Plan A sorties.",
                "observed_time": "2026-10-05T10:30:00Z"
            },
            {
                "id": "INS-02",
                "category": "SINGLE_POINT_OF_DEPENDENCY",
                "title": "Tanker A12 Single Point of Failure",
                "severity": "HIGH",
                "confidence": 0.91,
                "description": "Three concurrent patrol missions (M003, M007, M011) solely rely on Platform A12 for mid-flight refuel.",
                "observed_time": "2026-10-05T10:28:00Z"
            }
        ]
    }

@router.get("/timeline")
def get_timeline(minutes: int = 15, user: dict = Depends(require_permission("command:read"))):
    return state_engine.get_projections(minutes)
