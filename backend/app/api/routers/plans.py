from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
from app.services.optimizer import optimizer_service
from app.services.explanation_engine import explanation_service
from app.api.deps import require_permission

router = APIRouter(prefix="/plans", tags=["Operational Planning"])

class GeneratePlanRequest(BaseModel):
    horizon_hours: int = 4
    weights: Optional[Dict[str, float]] = None

@router.post("/generate")
def generate_plans(req: GeneratePlanRequest, user: dict = Depends(require_permission("plans:create"))):
    return optimizer_service.generate_plans(req.horizon_hours, req.weights)

@router.get("/active")
def get_active_plan(user: dict = Depends(require_permission("plans:read"))):
    plans = optimizer_service.generate_plans()
    return plans["plans"][1]  # Plan B accepted

@router.get("/explain/{plan_id}")
def explain_plan(plan_id: str, user: dict = Depends(require_permission("plans:read"))):
    return explanation_service.explain_plan(plan_id)
