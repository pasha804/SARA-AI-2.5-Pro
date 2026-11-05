# -*- coding: utf-8 -*-
"""
Automated unit tests for SARA's Controlled Self-Improvement System.
Tests system health assessment, proposal creation, duplicate detection, and loop prevention.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

from sara_self_improvement import SelfImprovementEngine, MAX_RETRIES_PER_MODULE


class TestSelfImprovement(unittest.TestCase):

    def setUp(self):
        self.engine = SelfImprovementEngine()

    def test_01_evaluate_system_capabilities(self):
        """Verify capability evaluator runs and writes weekly assessment report."""
        res = self.engine.evaluate_system_capabilities()
        self.assertIn("assessment_id", res)
        self.assertIn("overall_health", res)
        self.assertIn("metrics", res)

    def test_02_create_proposal_and_loop_prevention(self):
        """Verify proposal creation and loop prevention max retries guard."""
        comp = "TestSubsystem"
        prob = "Sample test defect for unit testing"
        sol = "Implement unit fix"

        # 1. Initial creation
        p1 = self.engine.create_upgrade_proposal(comp, prob, sol, ["test.py"])
        self.assertTrue(p1["success"])
        prop_id = p1["proposal"]["proposal_id"]

        # 2. Trigger retries up to max
        for _ in range(MAX_RETRIES_PER_MODULE - 1):
            self.engine.create_upgrade_proposal(comp, prob, sol, ["test.py"])

        # 3. Next retry should be rejected by loop prevention
        rejection = self.engine.create_upgrade_proposal(comp, prob, sol, ["test.py"])
        self.assertFalse(rejection["success"])
        self.assertTrue(rejection.get("rejected", False))
        self.assertIn("Loop prevention triggered", rejection.get("reason", ""))

        # Cleanup
        if prop_id in self.engine.proposals["active"]:
            del self.engine.proposals["active"][prop_id]
            self.engine.save_proposals()


if __name__ == "__main__":
    unittest.main()
