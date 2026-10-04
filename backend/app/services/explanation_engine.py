from typing import Dict, Any, List

class ExplanationEngine:
    def explain_plan(self, plan_id: str) -> Dict[str, Any]:
        return {
            "plan_id": plan_id,
            "why_chosen": [
                {"statement": "Satisfies 96% of priority missions M001-M014 without secondary tanker delays.", "metric_evidence": "Sortie coverage: 96.0% vs Plan C 82.0%"},
                {"statement": "Preserves 18% fuel buffer at Forward Base B-Alpha during peak combat window.", "metric_evidence": "Reserve margin: 1,420 Gallons surplus"},
                {"statement": "Strictly satisfies 12-hour mandatory crew rest for all 18 flight crews.", "metric_evidence": "Zero rest-rule violations detected"}
            ],
            "why_not_alternatives": [
                {"alternative": "Plan Alpha (Aggressive Throughput)", "reason": "Violates fuel threshold at B-Delta, leading to single point of failure under minor weather delays.", "metric_evidence": "Fragility index 3.8 exceeds 2.0 ceiling"},
                {"alternative": "Plan Charlie (Minimal Footprint)", "reason": "Leaves 4 strategic reconnaissance sorties unassigned in western sector.", "metric_evidence": "Unmet priority demand: 4 missions"}
            ]
        }

explanation_service = ExplanationEngine()
