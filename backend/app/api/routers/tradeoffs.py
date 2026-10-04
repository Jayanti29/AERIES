from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.optimizer import optimizer_service
from app.api.deps import require_permission

router = APIRouter(prefix="/tradeoffs", tags=["Trade-off Explorer"])

class TradeoffRequest(BaseModel):
    coverage_vs_conservation: float
    efficiency_vs_resilience: float
    immediate_vs_flexibility: float

@router.post("/explore")
def explore_tradeoffs(req: TradeoffRequest, user: dict = Depends(require_permission("tradeoffs:explore"))):
    return optimizer_service.compute_tradeoffs(
        req.coverage_vs_conservation,
        req.efficiency_vs_resilience,
        req.immediate_vs_flexibility
    )
