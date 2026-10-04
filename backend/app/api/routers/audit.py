from fastapi import APIRouter, Depends
from app.core.audit import audit_service
from app.api.deps import require_permission

router = APIRouter(prefix="/audit", tags=["Governance & Audit"])

@router.get("/logs")
def get_logs(limit: int = 50, user: dict = Depends(require_permission("audit:read"))):
    return audit_service.get_logs(limit)

@router.post("/verify")
def verify_audit_chain(user: dict = Depends(require_permission("audit:verify"))):
    return audit_service.verify_chain()
