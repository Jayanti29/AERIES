from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.state_engine import state_engine
from app.core.security import decrypt_field
from app.core.audit import audit_service
from app.api.deps import require_permission, get_current_user

router = APIRouter(prefix="/people", tags=["Personnel Operations"])

class UnmaskRequest(BaseModel):
    person_code: str
    justification_reason: str

@router.get("/summary")
def get_people_summary(user: dict = Depends(require_permission("people:read"))):
    people = state_engine.data["personnel"]
    avail = sum(1 for p in people if p["status"] == "AVAILABLE")
    overloaded = sum(1 for p in people if p["status"] == "OVERLOADED")
    return {
        "personnel_total": len(people),
        "personnel_available": avail,
        "personnel_overloaded": overloaded,
        "average_workload_pct": 68.4,
        "qualification_gaps": 2
    }

@router.get("/roster")
def get_roster(user: dict = Depends(require_permission("people:read"))):
    # Mask real identities by default for data privacy
    return [
        {
            "code": p["code"],
            "callsign": p["callsign"],
            "masked_name": p["masked_name"],
            "team": p["team"],
            "role": p["role"],
            "status": p["status"],
            "workload_pct": p["workload_pct"],
            "duty_hours_today": p["duty_hours_today"],
            "qualifications": p["qualifications"]
        }
        for p in state_engine.data["personnel"]
    ]

@router.post("/unmask")
def unmask_person(req: UnmaskRequest, user: dict = Depends(require_permission("people:unmask"))):
    if len(req.justification_reason.strip()) < 10:
        raise HTTPException(status_code=400, detail="A detailed operational reason is mandatory for unmasking PII.")

    for p in state_engine.data["personnel"]:
        if p["code"] == req.person_code:
            key_hex = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
            unmasked_name = decrypt_field(p["encrypted_real_name"], key_hex)
            audit_service.record_event(
                user["id"], user["role"], "PII_UNMASK_ACCESSED", "PERSONNEL", p["code"],
                {"reason": req.justification_reason}
            )
            return {"code": p["code"], "real_name": unmasked_name, "callsign": p["callsign"]}
    raise HTTPException(status_code=404, detail="Personnel not found")
