from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.dependency_graph import graph_service
from app.services.chaos_engine import chaos_service
from app.services.stress_tester import stress_service
from app.api.deps import require_permission

router = APIRouter(prefix="/resilience", tags=["Resilience & Simulation"])

class ChaosRequest(BaseModel):
    disruptions: List[Dict[str, Any]]

class StressRequest(BaseModel):
    plan_id: str = "PLAN-B-RESILIENCE"
    scenario_count: int = 1000
    seed: int = 42

@router.get("/graph")
def get_graph(user: dict = Depends(require_permission("graph:read"))):
    return graph_service.get_graph()

@router.post("/cascade")
def run_cascade(entity_id: str, user: dict = Depends(require_permission("graph:read"))):
    return graph_service.simulate_cascade(entity_id)

@router.post("/chaos")
def run_chaos(req: ChaosRequest, user: dict = Depends(require_permission("chaos:run"))):
    return chaos_service.run_scenario(req.disruptions)

@router.post("/stress")
def run_stress(req: StressRequest, user: dict = Depends(require_permission("stress:run"))):
    return stress_service.run_stress_test(req.plan_id, req.scenario_count, req.seed)
