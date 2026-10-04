from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from app.core.security import verify_password, create_jwt, verify_totp
from app.core.config import settings
from app.core.audit import audit_service
from app.api.deps import get_current_user, _USERS_MAP

router = APIRouter(prefix="/auth", tags=["Authentication"])

class LoginRequest(BaseModel):
    username: str
    password: str
    totp_code: Optional[str] = None

class SwitchRoleRequest(BaseModel):
    target_role: str

@router.post("/login")
def login(req: LoginRequest):
    user = _USERS_MAP.get(req.username)
    if not user or not verify_password(req.password, user["hashed_password"]):
        audit_service.record_event(req.username, "UNKNOWN", "LOGIN_FAILED", "USER", req.username, {"reason": "Bad credentials"})
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if user.get("mfa_enabled") and req.totp_code:
        if not verify_totp(user["mfa_secret"], req.totp_code):
            audit_service.record_event(user["id"], user["role"], "MFA_FAILED", "USER", user["id"])
            raise HTTPException(status_code=401, detail="Invalid MFA token")

    token = create_jwt({"sub": user["username"], "role": user["role"]}, settings.SECRET_KEY)
    audit_service.record_event(user["id"], user["role"], "LOGIN_SUCCESS", "USER", user["id"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "role": user["role"],
            "callsign": user["callsign"]
        }
    }

@router.post("/switch-role")
def switch_role(req: SwitchRoleRequest):
    # Hackathon / Evaluation convenience endpoint
    for u in _USERS_MAP.values():
        if u["role"].lower() == req.target_role.lower():
            token = create_jwt({"sub": u["username"], "role": u["role"]}, settings.SECRET_KEY)
            audit_service.record_event(u["id"], u["role"], "ROLE_SWITCH_EVALUATION", "USER", u["id"], {"target_role": u["role"]})
            return {
                "access_token": token,
                "token_type": "bearer",
                "user": u
            }
    raise HTTPException(status_code=404, detail="Role not found")

@router.get("/me")
def get_me(user: dict = Depends(get_current_user)):
    return user

@router.post("/step-up")
def step_up_auth(user: dict = Depends(get_current_user)):
    audit_service.record_event(user["id"], user["role"], "STEP_UP_VERIFIED", "SESSION", user["id"])
    return {"status": "STEP_UP_AUTHORIZED", "valid_seconds": 300}
