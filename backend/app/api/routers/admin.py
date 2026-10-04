from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.audit import audit_service
from app.services.crypto_service import crypto_service
from app.api.deps import require_permission, get_current_user

router = APIRouter(prefix="/admin", tags=["Administration"])

class RotateKeyRequest(BaseModel):
    new_key_hex: str

@router.get("/users")
def get_users(user: dict = Depends(require_permission("admin:users"))):
    return [
        {"username": "planner", "role": "Operations Planner", "status": "ACTIVE"},
        {"username": "authority", "role": "Decision Authority", "status": "ACTIVE"},
        {"username": "admin", "role": "Administrator", "status": "ACTIVE"}
    ]

@router.post("/keys/rotate")
def rotate_keys(req: RotateKeyRequest, user: dict = Depends(require_permission("admin:keys"))):
    audit_service.record_event(user["id"], user["role"], "KEY_ROTATION_EXECUTED", "CRYPTO_KEY", "ENVELOPE_KEY")
    return crypto_service.rotate_keys(req.new_key_hex)
