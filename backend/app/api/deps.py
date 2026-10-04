from fastapi import Depends, HTTPException, status, Header
from typing import Optional
from app.core.config import settings
from app.core.security import decode_jwt
from app.core.rbac import check_permission
from app.data.seed_generator import generate_seed_data

_seed = generate_seed_data()
_USERS_MAP = {u["username"]: u for u in _seed["users"]}

def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization:
        # Default to Operations Planner for quick interactive testing
        return _USERS_MAP["planner"]

    token = authorization.replace("Bearer ", "")
    try:
        payload = decode_jwt(token, settings.SECRET_KEY, settings.ALGORITHM)
        username = payload.get("sub")
        if username in _USERS_MAP:
            return _USERS_MAP[username]
    except Exception:
        pass
    return _USERS_MAP["planner"]

def require_permission(perm: str):
    def dependency(user: dict = Depends(get_current_user)):
        check_permission(user["role"], perm)
        return user
    return dependency
