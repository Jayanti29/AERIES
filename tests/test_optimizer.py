import unittest
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
