from enum import Enum
from typing import Dict, Set, List
try:
    from fastapi import HTTPException, status
except ImportError:
    class HTTPException(Exception):
        def __init__(self, status_code, detail):
            self.status_code = status_code
            self.detail = detail
            super().__init__(detail)
    class status:
        HTTP_403_FORBIDDEN = 403


class Role(str, Enum):
    ADMINISTRATOR = "Administrator"
    OPERATIONS_PLANNER = "Operations Planner"
    DECISION_AUTHORITY = "Decision Authority"
    ANALYST = "Analyst"
    AUDITOR = "Auditor"
    PILOT = "Pilot"
    CRAFT_OFFICER = "Craft Officer"
    SUPPLY_OFFICER = "Supply Officer"
    PERSONNEL_OFFICER = "Personnel Officer"

# Comprehensive Granular Permissions
ROLE_PERMISSIONS: Dict[Role, Set[str]] = {
    Role.ADMINISTRATOR: {
        "admin:manage", "admin:users", "admin:roles", "admin:approvals",
        "admin:keys", "admin:generator", "admin:read_only", "audit:read",
        "models:read", "data:read", "health:read"
    },
    Role.OPERATIONS_PLANNER: {
        "command:read", "map:read", "insights:read", "craft:read",
        "supply:read", "people:read", "missions:read", "plans:create",
        "plans:read", "tradeoffs:explore", "graph:read", "chaos:run",
        "stress:run", "data:read", "decisions:read"
    },
    Role.DECISION_AUTHORITY: {
        "command:read", "map:read", "insights:read", "craft:read",
        "supply:read", "people:read", "missions:read", "plans:read",
        "decisions:read", "decisions:queue", "decisions:approve",
        "decisions:modify", "decisions:reject", "decisions:sign",
        "replay:read", "graph:read", "data:read"
    },
    Role.ANALYST: {
        "command:read", "map:read", "insights:read", "craft:read",
        "supply:read", "people:read", "missions:read", "plans:read",
        "data:read", "models:read"
    },
    Role.AUDITOR: {
        "audit:read", "audit:verify", "audit:export", "decisions:read",
        "replay:read", "models:read"
    },
    Role.PILOT: {
        "state:read_own", "pilot:duty", "pilot:schedule", "pilot:rest",
        "pilot:qualifications", "notifications:read"
    },
    Role.CRAFT_OFFICER: {
        "craft:read", "craft:fleet", "craft:maintenance", "craft:components",
        "craft:predictions", "maintenance:flag", "insights:read_craft",
        "data:read_maintenance", "plans:read"
    },
    Role.SUPPLY_OFFICER: {
        "supply:read", "supply:resources", "supply:forecast", "supply:bottlenecks",
        "supply:stock", "resource:flag", "insights:read_supply",
        "data:read_supply", "plans:read"
    },
    Role.PERSONNEL_OFFICER: {
        "people:read", "people:roster", "people:readiness", "people:coverage",
        "people:availability", "people:workload", "people:unmask",
        "availability:flag", "insights:read_people", "data:read_people", "plans:read"
    }
}

def has_permission(role: str, permission: str) -> bool:
    try:
        r = Role(role)
        return permission in ROLE_PERMISSIONS.get(r, set())
    except ValueError:
        return False

def check_permission(user_role: str, required_permission: str):
    if not has_permission(user_role, required_permission):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Forbidden: Role '{user_role}' lacks required permission '{required_permission}'"
        )
