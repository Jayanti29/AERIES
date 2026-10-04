from fastapi import APIRouter, Depends
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
