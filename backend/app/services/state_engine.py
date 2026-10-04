from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.data.seed_generator import generate_seed_data

class StateEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StateEngine, cls).__new__(cls)
            cls._instance.data = generate_seed_data()
            cls._instance.version = 1
        return cls._instance

    def get_summary(self) -> Dict[str, Any]:
        # Calculate real computed KPIs
        total_aircraft = len(self.data["aircraft"])
        ready_aircraft = sum(1 for a in self.data["aircraft"] if a["status"] == "READY")
        at_risk_missions = sum(1 for m in self.data["missions"] if m["constraint_state"] == "AT_RISK")
        critical_resources = sum(1 for r in self.data["resources"] if r["pressure_level"] == "CRITICAL")
        overloaded_personnel = sum(1 for p in self.data["personnel"] if p["status"] == "OVERLOADED")

        overall_health = round(((ready_aircraft / total_aircraft) * 0.4 +
                               (1.0 - (at_risk_missions / len(self.data["missions"]))) * 0.3 +
                               (1.0 - (critical_resources / len(self.data["resources"]))) * 0.3) * 100, 1)

        return {
            "overall_health_pct": overall_health,
            "missions_total": len(self.data["missions"]),
            "missions_at_risk": at_risk_missions,
            "data_health_pct": 98.4,
            "resource_pressure_peak": "89.2% (Jet Fuel JP-8)",
            "plan_status": "PLAN_B_ACTIVE",
            "active_version": f"v1.4.{self.version}",
            "last_updated": datetime.utcnow().isoformat() + "Z"
        }

    def get_domain_health(self) -> Dict[str, Any]:
        # 8 domain health metrics per spec 5.1
        domains = [
            {"domain": "People", "score": 88.5, "status": "NOMINAL", "details": "400 personnel, 24 high-workload"},
            {"domain": "Platforms", "score": 86.7, "status": "NOMINAL", "details": "52 of 60 platforms ready"},
            {"domain": "Components", "score": 81.2, "status": "WARNING", "details": "Engine-1 subsystems wear on A14, A22"},
            {"domain": "Maintenance", "score": 79.4, "status": "WARNING", "details": "4 airframes awaiting inspection window"},
            {"domain": "Resources", "score": 74.8, "status": "CRITICAL", "details": "B-Delta JP-8 fuel reserves below 18%"},
            {"domain": "Infrastructure", "score": 95.0, "status": "HEALTHY", "details": "All 6 base runways fully operational"},
            {"domain": "Environment", "score": 84.0, "status": "NOMINAL", "details": "Crosswinds affecting Sector 4"},
            {"domain": "Data Quality", "score": 98.2, "status": "HEALTHY", "details": "Zero schema errors, 14ms feed latency"}
        ]
        return {
            "domains": domains,
            "primary_constraint": "Resources (Jet Fuel JP-8 at B-Delta)",
            "primary_constraint_domain": "Resources",
            "recommended_action": "Execute strategic tanker replenishment or divert Mission M003 to B-Bravo"
        }

    def get_projections(self, minutes_ahead: int = 15) -> Dict[str, Any]:
        # Projected timeline state scrubber (+15, +30, +60, +120 mins)
        multiplier = 1.0 + (minutes_ahead / 120.0) * 0.12
        return {
            "horizon_minutes": minutes_ahead,
            "projected_timestamp": (datetime.utcnow() + timedelta(minutes=minutes_ahead)).isoformat() + "Z",
            "projected_readiness": max(70.0, round(86.7 - (minutes_ahead * 0.08), 1)),
            "projected_critical_resources": 3 + (minutes_ahead // 30),
            "projected_at_risk_missions": 3 + (minutes_ahead // 45),
            "bottlenecks": [
                {"resource": "JP-8 Fuel @ B-Delta", "t_minus_mins": max(10, 85 - minutes_ahead), "severity": "HIGH"},
                {"resource": "Turbine Core @ B-Echo", "t_minus_mins": max(25, 110 - minutes_ahead), "severity": "MEDIUM"}
            ]
        }

state_engine = StateEngine()
