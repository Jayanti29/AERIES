from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from app.core.security import sign_data
from app.core.audit import audit_service
from app.api.deps import require_permission, get_current_user

router = APIRouter(prefix="/decisions", tags=["Decision Authority Queue"])

class DecisionActionRequest(BaseModel):
    plan_id: str
    action: str  # ACCEPT, MODIFY, REJECT
    reason: str

@router.get("/queue")
def get_decision_queue(user: dict = Depends(require_permission("decisions:queue"))):
    return {
        "pending_submissions": [
            {
                "submission_id": "SUB-2026-001",
                "plan_id": "PLAN-B-RESILIENCE",
                "submitted_by": "planner",
                "submitted_at": "2026-10-05T09:45:00Z",
                "staleness_status": "FRESH",
                "staleness_minutes": 12,
                "data_confidence": 0.98
            }
        ]
    }

@router.post("/review")
def review_decision(req: DecisionActionRequest, user: dict = Depends(require_permission("decisions:approve"))):
    # Separation of duties: Planners cannot approve own plans
    if user["role"] == "Operations Planner":
        raise HTTPException(status_code=403, detail="Separation of Duties violation: Planners cannot approve plans.")

    key_hex = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    signature = sign_data(f"{req.plan_id}_{req.action}_{user['username']}", key_hex)

    audit_service.record_event(
        user["id"], user["role"], f"PLAN_{req.action}", "PLAN", req.plan_id,
        {"reason": req.reason, "signature": signature}
    )

    return {
        "status": f"PLAN_{req.action}_EXECUTED",
        "plan_id": req.plan_id,
        "signature": signature,
        "approved_by": user["username"]
    }
