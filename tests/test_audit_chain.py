import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.audit import AuditLedger

class TestAuditChain(unittest.TestCase):
    def test_hash_chain_integrity(self):
        ledger = AuditLedger()
        # Record three events
        ledger.record_event("usr-test", "Operations Planner", "TEST_EVENT_1", "RESOURCE", "R01")
        ledger.record_event("usr-test", "Decision Authority", "TEST_EVENT_2", "PLAN", "PLAN-B")

        verification = ledger.verify_chain()
        self.assertTrue(verification["valid"], f"Chain verification failed: {verification.get('reason')}")

    def test_tamper_detection(self):
        ledger = AuditLedger()
        ledger.record_event("usr-test", "Operations Planner", "ORIGINAL_ACTION", "RESOURCE", "R01")

        # Verify initial valid state
        self.assertTrue(ledger.verify_chain()["valid"])

        # Tamper with an existing record details
        tamper_idx = len(ledger.ledger) - 1
        ledger.ledger[tamper_idx]["action"] = "TAMPERED_ACTION"

        # Verification must now immediately catch the discrepancy
        tampered_result = ledger.verify_chain()
        self.assertFalse(tampered_result["valid"])
        self.assertEqual(tampered_result["tampered_index"], tamper_idx)

        # Restore ledger
        ledger.ledger[tamper_idx]["action"] = "ORIGINAL_ACTION"

if __name__ == '__main__':
    unittest.main()
