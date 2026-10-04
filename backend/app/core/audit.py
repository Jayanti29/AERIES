import hashlib
import json
import time
from typing import Optional, Dict, Any, List
from datetime import datetime

class AuditLedger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuditLedger, cls).__new__(cls)
            cls._instance.ledger = []
            cls._instance._init_genesis()
        return cls._instance

    def _init_genesis(self):
        genesis_entry = {
            "index": 0,
            "timestamp": "2026-10-05T00:00:00Z",
            "actor_id": "SYSTEM_CORE",
            "actor_role": "SYSTEM",
            "action": "GENESIS_LEDGER_INIT",
            "resource_type": "LEDGER",
            "resource_id": "CHAIN_0",
            "details": {"status": "AERIS Ledger Initialized", "version": "1.0"},
            "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000",
            "current_hash": ""
        }
        genesis_entry["current_hash"] = self._compute_hash(genesis_entry)
        self.ledger.append(genesis_entry)

    def _compute_hash(self, entry: Dict[str, Any]) -> str:
        payload = f"{entry['index']}|{entry['timestamp']}|{entry['actor_id']}|{entry['actor_role']}|{entry['action']}|{entry['resource_type']}|{entry['resource_id']}|{json.dumps(entry['details'], sort_keys=True)}|{entry['prev_hash']}"
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()

    def record_event(
        self,
        actor_id: str,
        actor_role: str,
        action: str,
        resource_type: str,
        resource_id: str,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        prev_entry = self.ledger[-1]
        new_entry = {
            "index": len(self.ledger),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "actor_id": actor_id,
            "actor_role": actor_role,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "details": details or {},
            "prev_hash": prev_entry["current_hash"],
            "current_hash": ""
        }
        new_entry["current_hash"] = self._compute_hash(new_entry)
        self.ledger.append(new_entry)
        return new_entry

    def verify_chain(self) -> Dict[str, Any]:
        if not self.ledger:
            return {"valid": False, "reason": "Ledger is empty", "tampered_index": None}

        # Check genesis
        first = self.ledger[0]
        if first["prev_hash"] != "0000000000000000000000000000000000000000000000000000000000000000":
            return {"valid": False, "reason": "Invalid genesis block", "tampered_index": 0}

        calc_first_hash = self._compute_hash(first)
        if calc_first_hash != first["current_hash"]:
            return {"valid": False, "reason": "Genesis hash corrupted", "tampered_index": 0}

        for i in range(1, len(self.ledger)):
            prev = self.ledger[i - 1]
            curr = self.ledger[i]

            if curr["prev_hash"] != prev["current_hash"]:
                return {
                    "valid": False,
                    "reason": f"Hash chain broken at index {i}",
                    "tampered_index": i
                }

            expected_hash = self._compute_hash(curr)
            if curr["current_hash"] != expected_hash:
                return {
                    "valid": False,
                    "reason": f"Hash signature invalid at index {i}",
                    "tampered_index": i
                }

        return {
            "valid": True,
            "reason": "All cryptographic links verified successfully",
            "total_records": len(self.ledger),
            "chain_head": self.ledger[-1]["current_hash"]
        }

    def get_logs(self, limit: int = 100, action_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        logs = self.ledger[::-1]
        if action_filter:
            logs = [entry for entry in logs if action_filter.lower() in entry["action"].lower()]
        return logs[:limit]

audit_service = AuditLedger()
