from typing import Dict, Any, List

class MLPredictorService:
    def get_maintenance_predictions(self) -> List[Dict[str, Any]]:
        return [
            {
                "aircraft_code": "A14",
                "subsystem": "Turbine Core (Engine 1)",
                "p_failure_15m": 0.04,
                "p_failure_60m": 0.18,
                "p_failure_120m": 0.42,
                "shap_contributions": [
                    {"feature": "Exhaust Gas Temp Exceedance", "impact": "+0.28"},
                    {"feature": "Total Flight Hours (3,120)", "impact": "+0.12"},
                    {"feature": "Hydraulic Pressure Stability", "impact": "-0.08"}
                ]
            },
            {
                "aircraft_code": "A22",
                "subsystem": "APG-81 Radar Array",
                "p_failure_15m": 0.02,
                "p_failure_60m": 0.09,
                "p_failure_120m": 0.27,
                "shap_contributions": [
                    {"feature": "Cooling Loop Differential", "impact": "+0.19"},
                    {"feature": "High Vibration Cycles", "impact": "+0.11"}
                ]
            }
        ]

ml_service = MLPredictorService()
