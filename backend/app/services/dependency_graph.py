from typing import Dict, Any, List

class DependencyGraphService:
    def __init__(self):
        self.nodes = [
            {"id": "B-Alpha", "label": "B-Alpha Station", "type": "BASE", "status": "HEALTHY"},
            {"id": "B-Delta", "label": "B-Delta Logistics", "type": "BASE", "status": "CRITICAL"},
            {"id": "A01", "label": "A01 Fighter", "type": "PLATFORM", "status": "HEALTHY"},
            {"id": "A12", "label": "A12 Tanker", "type": "PLATFORM", "status": "WARNING"},
            {"id": "A24", "label": "A24 Recon", "type": "PLATFORM", "status": "HEALTHY"},
            {"id": "R01_Delta", "label": "JP-8 Fuel (Delta)", "type": "RESOURCE", "status": "CRITICAL"},
            {"id": "R03_Delta", "label": "LOX (Delta)", "type": "RESOURCE", "status": "HEALTHY"},
            {"id": "P-0012", "label": "Lead Pilot 12", "type": "PERSONNEL", "status": "HEALTHY"},
            {"id": "P-0045", "label": "Weapons Tech 45", "type": "PERSONNEL", "status": "WARNING"},
            {"id": "M001", "label": "Sentinel Watch 1", "type": "MISSION", "status": "HEALTHY"},
            {"id": "M003", "label": "Sentinel Watch 3", "type": "MISSION", "status": "AT_RISK"}
        ]

        self.edges = [
            {"source": "B-Delta", "target": "R01_Delta", "label": "STOCKS"},
            {"source": "B-Delta", "target": "R03_Delta", "label": "STOCKS"},
            {"source": "R01_Delta", "target": "A12", "label": "FUELS"},
            {"source": "A12", "target": "M003", "label": "SUPPORTS"},
            {"source": "P-0012", "target": "A01", "label": "CREWS"},
            {"source": "P-0045", "target": "A12", "label": "SERVICES"},
            {"source": "A01", "target": "M001", "label": "EXECUTES"},
            {"source": "B-Alpha", "target": "A01", "label": "HOUSES"}
        ]

    def get_graph(self) -> Dict[str, Any]:
        return {
            "nodes": self.nodes,
            "edges": self.edges,
            "single_points_of_dependency": [
                {"entity_id": "R01_Delta", "type": "RESOURCE", "impact_reach": 4, "description": "Single fuel source for Tanker A12 and dependent patrol missions"}
            ]
        }

    def simulate_cascade(self, failed_entity_id: str) -> Dict[str, Any]:
        affected = [failed_entity_id]
        if failed_entity_id in ["R01_Delta", "B-Delta"]:
            affected.extend(["A12", "M003"])
        elif failed_entity_id == "A01":
            affected.append("M001")

        return {
            "root_failure": failed_entity_id,
            "cascade_path": affected,
            "affected_count": len(affected),
            "estimated_operational_degradation_pct": len(affected) * 14.5,
            "isolated_missions": [x for x in affected if x.startswith("M")]
        }

graph_service = DependencyGraphService()
