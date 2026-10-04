from typing import Dict, Any, List
import random

class ChaosEngine:
    DISRUPTION_TYPES = [
        "PLATFORM_AVAILABILITY",
        "PERSONNEL_AVAILABILITY",
        "RESOURCE_CAPACITY",
        "WEATHER_SEVERITY",
        "INFRASTRUCTURE_CAPACITY",
        "AIRSPACE_RESTRICTION",
        "MAINTENANCE_SURGE"
    ]

    def run_scenario(self, disruptions: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Calculate impact of disruptions
        total_mag = sum(d.get("magnitude", 0.5) for d in disruptions)
        affected_count = min(60, int(len(disruptions) * 8 * total_mag))
        degradation_pct = min(85.0, round(total_mag * 18.5, 1))

        return {
            "scenario_status": "COMPLETED",
            "events_injected": len(disruptions),
            "affected_platforms_count": min(60, int(affected_count * 0.4)),
            "affected_personnel_count": min(400, int(affected_count * 2.5)),
            "new_bottlenecks": [
                {"resource": "B-Delta JP-8", "status": "DEPLETED", "shortfall": "3,400 Gallons"},
                {"platform": "AEW&C Sentinel A16", "status": "GROUNDED", "reason": "Severe Weather in Sector 4"}
            ],
            "plan_degradation_pct": degradation_pct,
            "feasible_alternatives_count": 2,
            "recommended_retask": "Shift Mission M004 to B-Bravo and deploy Tanker A11"
        }

chaos_service = ChaosEngine()
