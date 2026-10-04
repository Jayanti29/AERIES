# Backend API Routers and Main Entrypoint for AERIS

def get_backend_routers():
    files = {}

    files['backend/app/api/routers/auth.py'] = """from fastapi import APIRouter, Depends, HTTPException, status
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
"""

    files['backend/app/api/routers/command.py'] = """from fastapi import APIRouter, Depends
from app.services.state_engine import state_engine
from app.api.deps import require_permission

router = APIRouter(prefix="/command", tags=["Command Center"])

@router.get("/summary")
def get_summary(user: dict = Depends(require_permission("command:read"))):
    return state_engine.get_summary()

@router.get("/health")
def get_health(user: dict = Depends(require_permission("command:read"))):
    return state_engine.get_domain_health()

@router.get("/map-layers")
def get_map_layers(user: dict = Depends(require_permission("map:read"))):
    return {
        "bases": state_engine.data["bases"],
        "aircraft": state_engine.data["aircraft"][:20],
        "airspace_zones": [
            {"code": "Z-01", "name": "Northern Corridor Alpha", "status": "CLEAR", "min_alt_ft": 10000, "max_alt_ft": 45000},
            {"code": "Z-02", "name": "Desert Strike Sector 4", "status": "RESTRICTED", "reason": "High Turbulence & Crosswinds"}
        ]
    }

@router.get("/insights")
def get_insights(user: dict = Depends(require_permission("insights:read"))):
    return {
        "insights": [
            {
                "id": "INS-01",
                "category": "HIDDEN_CONSTRAINT",
                "title": "B-Delta Fuel Reserve Exhaustion Risk",
                "severity": "CRITICAL",
                "confidence": 0.94,
                "description": "Jet Fuel draw rate at B-Delta exceeds inbound replenishment schedule by 22% under current Plan A sorties.",
                "observed_time": "2026-10-05T10:30:00Z"
            },
            {
                "id": "INS-02",
                "category": "SINGLE_POINT_OF_DEPENDENCY",
                "title": "Tanker A12 Single Point of Failure",
                "severity": "HIGH",
                "confidence": 0.91,
                "description": "Three concurrent patrol missions (M003, M007, M011) solely rely on Platform A12 for mid-flight refuel.",
                "observed_time": "2026-10-05T10:28:00Z"
            }
        ]
    }

@router.get("/timeline")
def get_timeline(minutes: int = 15, user: dict = Depends(require_permission("command:read"))):
    return state_engine.get_projections(minutes)
"""

    files['backend/app/api/routers/craft.py'] = """from fastapi import APIRouter, Depends
from app.services.state_engine import state_engine
from app.services.ml_predictor import ml_service
from app.api.deps import require_permission

router = APIRouter(prefix="/craft", tags=["Craft Operations"])

@router.get("/summary")
def get_craft_summary(user: dict = Depends(require_permission("craft:read"))):
    fleet = state_engine.data["aircraft"]
    ready = sum(1 for a in fleet if a["status"] == "READY")
    maint = sum(1 for a in fleet if a["status"] == "MAINTENANCE")
    return {
        "fleet_total": len(fleet),
        "fleet_ready": ready,
        "fleet_in_maintenance": maint,
        "average_readiness_pct": 91.4,
        "average_component_health": 88.6,
        "predicted_constraints_2h": 4
    }

@router.get("/fleet")
def get_fleet(user: dict = Depends(require_permission("craft:read"))):
    return state_engine.data["aircraft"]

@router.get("/maintenance")
def get_maintenance(user: dict = Depends(require_permission("craft:read"))):
    return [
        {"aircraft_code": "A14", "task": "Turbine Core 100-Hr Inspection", "scheduled": "2026-10-05T14:00:00Z", "status": "OVERDUE"},
        {"aircraft_code": "A22", "task": "Radar Array Calibration", "scheduled": "2026-10-05T16:30:00Z", "status": "UPCOMING"}
    ]

@router.get("/predictions")
def get_predictions(user: dict = Depends(require_permission("craft:read"))):
    return ml_service.get_maintenance_predictions()
"""

    files['backend/app/api/routers/supply.py'] = """from fastapi import APIRouter, Depends
from app.services.state_engine import state_engine
from app.api.deps import require_permission

router = APIRouter(prefix="/supply", tags=["Supply Logistics"])

@router.get("/summary")
def get_supply_summary(user: dict = Depends(require_permission("supply:read"))):
    stocks = state_engine.data["resources"]
    critical = sum(1 for s in stocks if s["pressure_level"] == "CRITICAL")
    elevated = sum(1 for s in stocks if s["pressure_level"] == "ELEVATED")
    return {
        "resource_types_tracked": 12,
        "resources_under_pressure": critical + elevated,
        "projected_shortfalls_2h": critical,
        "average_reserve_margin_pct": 28.5,
        "bases_with_constraints": ["B-Delta", "B-Echo"]
    }

@router.get("/resources")
def get_resources(user: dict = Depends(require_permission("supply:read"))):
    return state_engine.data["resources"]

@router.get("/forecast/{resource_id}")
def get_resource_forecast(resource_id: str, user: dict = Depends(require_permission("supply:read"))):
    return {
        "resource_id": resource_id,
        "projections": [
            {"horizon": "+15m", "demand": 4300, "capacity": 5000, "confidence_band": [4100, 4500]},
            {"horizon": "+30m", "demand": 4650, "capacity": 5000, "confidence_band": [4400, 4850]},
            {"horizon": "+60m", "demand": 5100, "capacity": 5000, "confidence_band": [4800, 5350]},
            {"horizon": "+120m", "demand": 5700, "capacity": 5000, "confidence_band": [5300, 6100]}
        ],
        "threshold": 5000
    }
"""

    files['backend/app/api/routers/people.py'] = """from fastapi import APIRouter, Depends, HTTPException
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
"""

    files['backend/app/api/routers/pilot.py'] = """from fastapi import APIRouter, Depends
from app.api.deps import require_permission, get_current_user

router = APIRouter(prefix="/pilot", tags=["Pilot Individual Operations"])

@router.get("/me")
def get_pilot_duty(user: dict = Depends(require_permission("state:read_own"))):
    return {
        "callsign": user.get("callsign", "MAVERICK"),
        "role": "Lead Interceptor Pilot",
        "current_assignment": {
            "mission_code": "M001",
            "mission_name": "Operation Sentinel Watch 1",
            "aircraft_code": "A01",
            "base_code": "B-Alpha",
            "start_time": "2026-10-05T11:00:00Z",
            "end_time": "2026-10-05T15:00:00Z"
        },
        "readiness_status": "READY_FOR_SORTIE",
        "duty_hours_today": 3.5,
        "max_allowable_duty_hours": 8.0,
        "rest_hours_accumulated": 14.5
    }

@router.get("/me/schedule")
def get_pilot_schedule(user: dict = Depends(require_permission("state:read_own"))):
    return {
        "upcoming_sorties": [
            {"time": "Today 11:00 - 15:00 UTC", "event": "Combat Air Patrol Sortie Alpha", "code": "M001"},
            {"time": "Tomorrow 08:30 - 12:00 UTC", "event": "Tactical Intercept Briefing", "code": "M008"}
        ]
    }

@router.get("/me/notifications")
def get_pilot_notifications(user: dict = Depends(require_permission("state:read_own"))):
    return [
        {"timestamp": "2026-10-05T10:15:00Z", "title": "Sortie Window Adjusted", "details": "Mission M001 takeoff shifted +15 mins due to sector clearance."}
    ]
"""

    files['backend/app/api/routers/plans.py'] = """from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
from app.services.optimizer import optimizer_service
from app.services.explanation_engine import explanation_service
from app.api.deps import require_permission

router = APIRouter(prefix="/plans", tags=["Operational Planning"])

class GeneratePlanRequest(BaseModel):
    horizon_hours: int = 4
    weights: Optional[Dict[str, float]] = None

@router.post("/generate")
def generate_plans(req: GeneratePlanRequest, user: dict = Depends(require_permission("plans:create"))):
    return optimizer_service.generate_plans(req.horizon_hours, req.weights)

@router.get("/active")
def get_active_plan(user: dict = Depends(require_permission("plans:read"))):
    plans = optimizer_service.generate_plans()
    return plans["plans"][1]  # Plan B accepted

@router.get("/explain/{plan_id}")
def explain_plan(plan_id: str, user: dict = Depends(require_permission("plans:read"))):
    return explanation_service.explain_plan(plan_id)
"""

    files['backend/app/api/routers/tradeoffs.py'] = """from fastapi import APIRouter, Depends
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
"""

    files['backend/app/api/routers/decisions.py'] = """from fastapi import APIRouter, Depends, HTTPException
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
"""

    files['backend/app/api/routers/resilience.py'] = """from fastapi import APIRouter, Depends
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
"""

    files['backend/app/api/routers/audit.py'] = """from fastapi import APIRouter, Depends
from app.core.audit import audit_service
from app.api.deps import require_permission

router = APIRouter(prefix="/audit", tags=["Governance & Audit"])

@router.get("/logs")
def get_logs(limit: int = 50, user: dict = Depends(require_permission("audit:read"))):
    return audit_service.get_logs(limit)

@router.post("/verify")
def verify_audit_chain(user: dict = Depends(require_permission("audit:verify"))):
    return audit_service.verify_chain()
"""

    files['backend/app/api/routers/flags.py'] = """from fastapi import APIRouter, Depends, HTTPException
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
"""

    files['backend/app/api/routers/admin.py'] = """from fastapi import APIRouter, Depends
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
"""

    files['backend/app/main.py'] = """from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
from app.core.config import settings
from app.api.routers import (
    auth, command, craft, supply, people, pilot,
    plans, tradeoffs, decisions, resilience, audit, flags, admin
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security Headers Middleware
@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start_time) * 1000, 2)

    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Handling-Banner"] = settings.HANDLING_BANNER
    response.headers["X-Response-Time-Ms"] = str(duration_ms)
    return response

# Register API Routers
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(command.router, prefix=settings.API_PREFIX)
app.include_router(craft.router, prefix=settings.API_PREFIX)
app.include_router(supply.router, prefix=settings.API_PREFIX)
app.include_router(people.router, prefix=settings.API_PREFIX)
app.include_router(pilot.router, prefix=settings.API_PREFIX)
app.include_router(plans.router, prefix=settings.API_PREFIX)
app.include_router(tradeoffs.router, prefix=settings.API_PREFIX)
app.include_router(decisions.router, prefix=settings.API_PREFIX)
app.include_router(resilience.router, prefix=settings.API_PREFIX)
app.include_router(audit.router, prefix=settings.API_PREFIX)
app.include_router(flags.router, prefix=settings.API_PREFIX)
app.include_router(admin.router, prefix=settings.API_PREFIX)

@app.get("/api/health")
def health_check():
    return {
        "status": "HEALTHY",
        "handling_banner": settings.HANDLING_BANNER,
        "version": settings.VERSION
    }
"""

    return files

print("backend_routers.py loaded")
