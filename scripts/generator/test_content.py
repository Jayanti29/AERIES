# Test Suite Generators for AERIS

def get_test_files():
    files = {}

    files['tests/test_auth_matrix.py'] = """import unittest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.rbac import Role, ROLE_PERMISSIONS, has_permission

class TestAuthMatrix(unittest.TestCase):
    def test_deny_by_default(self):
        # A random role or permission should strictly deny
        self.assertFalse(has_permission("Guest", "command:read"))
        self.assertFalse(has_permission(Role.PILOT, "craft:maintenance"))

    def test_planner_cannot_approve(self):
        # Spec rule: Planners cannot approve own plans
        self.assertTrue(has_permission(Role.OPERATIONS_PLANNER, "plans:create"))
        self.assertFalse(has_permission(Role.OPERATIONS_PLANNER, "decisions:approve"))

    def test_authority_cannot_create_plans(self):
        # Spec rule: Decision Authority approves plans, cannot create plans
        self.assertTrue(has_permission(Role.DECISION_AUTHORITY, "decisions:approve"))
        self.assertFalse(has_permission(Role.DECISION_AUTHORITY, "plans:create"))

    def test_pilot_own_data_only(self):
        # Pilot can only see own state
        self.assertTrue(has_permission(Role.PILOT, "state:read_own"))
        self.assertFalse(has_permission(Role.PILOT, "people:read"))
        self.assertFalse(has_permission(Role.PILOT, "craft:read"))

    def test_personnel_unmask_restricted(self):
        # Only Personnel Officer has people:unmask permission
        self.assertTrue(has_permission(Role.PERSONNEL_OFFICER, "people:unmask"))
        self.assertFalse(has_permission(Role.CRAFT_OFFICER, "people:unmask"))
        self.assertFalse(has_permission(Role.SUPPLY_OFFICER, "people:unmask"))

if __name__ == '__main__':
    unittest.main()
"""

    files['tests/test_audit_chain.py'] = """import unittest
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
"""

    files['tests/test_optimizer.py'] = """import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.services.optimizer import OptimizerService

class TestOptimizer(unittest.TestCase):
    def setUp(self):
        self.optimizer = OptimizerService()

    def test_plans_generated_have_differing_dna(self):
        res = self.optimizer.generate_plans()
        plans = res["plans"]
        self.assertEqual(len(plans), 3)

        plan_a = plans[0]
        plan_b = plans[1]
        plan_c = plans[2]

        # Plan A should have highest efficiency
        self.assertGreater(plan_a["dna"]["efficiency"], plan_c["dna"]["efficiency"])
        # Plan B should have highest resilience
        self.assertGreater(plan_b["dna"]["resilience"], plan_a["dna"]["resilience"])
        # Plan C should have highest resource reserve
        self.assertGreater(plan_c["dna"]["resource_reserve"], plan_a["dna"]["resource_reserve"])

    def test_tradeoffs_recalculation(self):
        t1 = self.optimizer.compute_tradeoffs(0.1, 0.1, 0.5)
        t2 = self.optimizer.compute_tradeoffs(0.9, 0.9, 0.5)

        # Higher coverage slider should yield higher candidate coverage
        self.assertGreater(t2["candidate_dna"]["coverage"], t1["candidate_dna"]["coverage"])
        # Higher resilience slider should yield lower fragility index
        self.assertLess(t2["fragility_index"], t1["fragility_index"])

if __name__ == '__main__':
    unittest.main()
"""

    files['tests/test_field_encryption.py'] = """import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.security import encrypt_field, decrypt_field

class TestFieldEncryption(unittest.TestCase):
    def test_encryption_roundtrip(self):
        key_hex = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
        secret_name = "Major Johnathan Synthetic Pilot"

        ciphertext = encrypt_field(secret_name, key_hex)
        self.assertTrue(ciphertext.startswith("enc:"))
        self.assertNotEqual(secret_name, ciphertext)

        decrypted = decrypt_field(ciphertext, key_hex)
        self.assertEqual(secret_name, decrypted)

    def test_decryption_with_wrong_key_fails_safely(self):
        key1 = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
        key2 = "fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210"
        secret = "Classified Personnel 42"

        ciphertext = encrypt_field(secret, key1)
        decrypted = decrypt_field(ciphertext, key2)
        # Should not reveal the plaintext
        self.assertNotEqual(secret, decrypted)

if __name__ == '__main__':
    unittest.main()
"""

    files['tests/test_cascade.py'] = """import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.services.dependency_graph import DependencyGraphService

class TestCascade(unittest.TestCase):
    def test_cascade_simulation(self):
        graph = DependencyGraphService()
        cascade = graph.simulate_cascade("R01_Delta")

        self.assertIn("A12", cascade["cascade_path"])
        self.assertIn("M003", cascade["cascade_path"])
        self.assertGreater(cascade["estimated_operational_degradation_pct"], 0.0)

if __name__ == '__main__':
    unittest.main()
"""

    return files

print("test_content.py loaded")
