from typing import Dict, Any, List
import copy

class OptimizerService:
    def generate_plans(self, horizon_hours: int = 4, weights: Dict[str, float] = None) -> Dict[str, Any]:
        # Formulate Plans A, B, and C with distinct Plan DNA
        w = weights or {"efficiency": 0.5, "resilience": 0.5, "conservation": 0.5}

        plan_a = {
            "id": "PLAN-A-EFFICIENCY",
            "name": "Plan Alpha (Operational Efficiency)",
            "description": "Maximizes mission sortie rate and throughput while running tight resource buffers.",
            "dna": {
                "coverage": 96.0,
                "efficiency": 94.0,
                "resilience": 68.0,
                "flexibility": 64.0,
                "speed": 92.0,
                "resource_reserve": 58.0
            },
            "metrics": {
                "missions_assigned": 24,
                "unmet_demand": 0,
                "fuel_burn_gal": 42000,
                "crew_rest_violations": 0,
                "fragility_score": 3.8
            },
            "status": "CANDIDATE"
        }

        plan_b = {
            "id": "PLAN-B-RESILIENCE",
            "name": "Plan Bravo (Resilient Redundancy)",
            "description": "Maintains dedicated backup aircraft on alert and spreads fuel draw across auxiliary bases.",
            "dna": {
                "coverage": 91.0,
                "efficiency": 82.0,
                "resilience": 94.0,
                "flexibility": 89.0,
                "speed": 85.0,
                "resource_reserve": 81.0
            },
            "metrics": {
                "missions_assigned": 23,
                "unmet_demand": 1,
                "fuel_burn_gal": 46500,
                "crew_rest_violations": 0,
                "fragility_score": 1.4
            },
            "status": "ACCEPTED"
        }

        plan_c = {
            "id": "PLAN-C-CONSERVATION",
            "name": "Plan Charlie (Minimal Footprint)",
            "description": "Minimizes platform flight hours and maintains max reserve stocks for emergency surge.",
            "dna": {
                "coverage": 82.0,
                "efficiency": 74.0,
                "resilience": 78.0,
                "flexibility": 76.0,
                "speed": 72.0,
                "resource_reserve": 95.0
            },
            "metrics": {
                "missions_assigned": 20,
                "unmet_demand": 4,
                "fuel_burn_gal": 31000,
                "crew_rest_violations": 0,
                "fragility_score": 2.2
            },
            "status": "CANDIDATE"
        }

        return {
            "plans": [plan_a, plan_b, plan_c],
            "recommended_plan": "PLAN-B-RESILIENCE",
            "accepted_plan_id": "PLAN-B-RESILIENCE"
        }

    def compute_tradeoffs(self, coverage_vs_conservation: float, efficiency_vs_resilience: float, immediate_vs_flex: float) -> Dict[str, Any]:
        # Live recalculation from trade-off sliders
        cov = round(70 + coverage_vs_conservation * 25, 1)
        res = round(60 + efficiency_vs_resilience * 35, 1)
        eff = round(95 - efficiency_vs_resilience * 20, 1)
        reserves = round(95 - coverage_vs_conservation * 35, 1)

        return {
            "candidate_dna": {
                "coverage": cov,
                "efficiency": eff,
                "resilience": res,
                "flexibility": round(65 + immediate_vs_flex * 25, 1),
                "speed": round(80 + immediate_vs_flex * 15, 1),
                "resource_reserve": reserves
            },
            "projected_missions_satisfied": int(cov / 100 * 24),
            "projected_reserve_margin_pct": reserves,
            "fragility_index": round((100 - res) / 10, 2)
        }

optimizer_service = OptimizerService()
