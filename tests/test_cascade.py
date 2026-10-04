import unittest
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
