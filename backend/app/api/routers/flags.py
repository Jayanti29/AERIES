from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.audit import audit_service
from app.api.deps import require_permission, get_current_user

router = APIRouter(prefix="/flags", tags=["Operational Flagging Actions"])

class FlagRequest(BaseModel):
    entity_code: str
    flag_type: str
    reason: str

@router.post("/maintenance")
def flag_maintenance(req: FlagRequest, user: dict = Depends(require_permission("maintenance:flag"))):
    if len(req.reason.strip()) < 5:
        raise HTTPException(status_code=400, detail="Reason required")
    audit_service.record_event(user["id"], user["role"], "MAINTENANCE_FLAGGED", "AIRCRAFT", req.entity_code, {"reason": req.reason})
    return {"status": "FLAGGED", "entity": req.entity_code, "action": "MAINTENANCE_EVENT_QUEUED"}

@router.post("/resource")
def flag_resource(req: FlagRequest, user: dict = Depends(require_permission("resource:flag"))):
    audit_service.record_event(user["id"], user["role"], "RESOURCE_FLAGGED", "RESOURCE", req.entity_code, {"reason": req.reason})
    return {"status": "FLAGGED", "entity": req.entity_code, "action": "RESOURCE_INSPECTION_QUEUED"}

@router.post("/availability")
def flag_availability(req: FlagRequest, user: dict = Depends(require_permission("availability:flag"))):
    audit_service.record_event(user["id"], user["role"], "AVAILABILITY_FLAGGED", "PERSONNEL", req.entity_code, {"reason": req.reason})
    return {"status": "FLAGGED", "entity": req.entity_code, "action": "ROSTER_STATUS_UPDATED"}
