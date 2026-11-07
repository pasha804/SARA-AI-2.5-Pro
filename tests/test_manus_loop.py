# -*- coding: utf-8 -*-
import os
import sys
import unittest
from pathlib import Path

BASE_DIR = Path(r"D:\MARAA AI").resolve()
sys.path.insert(0, str(BASE_DIR))

from sara_manus_loop import manus_agent, MANUS_DIR


class TestManusAutonomousAgentLoop(unittest.TestCase):

    def test_goal_decomposition(self):
        """Test breaking high-level goal into structured sequential steps."""
        goal = "Research competitors, write a Word report, create a slide deck, and announce on Discord"
        steps = manus_agent.decompose_goal(goal)
        self.assertGreaterEqual(len(steps), 3)
        actions = [s["action"] for s in steps]
        self.assertIn("browser_search", actions)
        self.assertIn("create_word_document", actions)
        self.assertIn("create_presentation", actions)

    def test_end_to_end_manus_execution(self):
        """Test end-to-end multi-step autonomous execution and artifact generation."""
        goal = "Research AI agentic systems, write a Word documentation, and create a slide deck"
        res = manus_agent.run_goal_loop(goal)
        self.assertTrue(res.get("success"))
        self.assertEqual(res.get("completed_steps"), res.get("total_steps"))
        self.assertGreaterEqual(len(res.get("artifacts", [])), 2)
        self.assertTrue(Path(res.get("session_file")).exists())
        self.assertIn("Pasha Jan", res.get("spoken_reply", ""))

        # Verify active session tracking
        active = manus_agent.get_active_session()
        self.assertEqual(active.get("status"), "COMPLETED")
        self.assertEqual(active.get("progress_pct"), 100)


if __name__ == "__main__":
    unittest.main()

