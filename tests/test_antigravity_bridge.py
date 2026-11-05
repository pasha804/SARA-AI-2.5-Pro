# -*- coding: utf-8 -*-
"""
Automated unit tests for SARA's Antigravity Autonomous Development Bridge.
Tests detection, task preparation, task submission, and verification routines.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

from sara_antigravity_bridge import AntigravityBridge, TASKS_DATA_DIR


class TestAntigravityBridge(unittest.TestCase):

    def setUp(self):
        self.bridge = AntigravityBridge()

    def test_01_detect_antigravity(self):
        """Verify Antigravity CLI detection on system."""
        status = self.bridge.detect_antigravity()
        self.assertIn("installed", status)
        self.assertIn("status", status)
        self.assertTrue(status["installed"], "Antigravity CLI (agy.exe) should be detected in this environment.")

    def test_02_prepare_development_task(self):
        """Verify task payload preparation and persistence."""
        task = self.bridge.prepare_development_task(
            objective="Unit Test Task",
            problem_statement="Testing bridge contract",
            expected_behavior="Passes cleanly",
            relevant_files=["tests/test_antigravity_bridge.py"]
        )
        self.assertIn("task_id", task)
        self.assertEqual(task["status"], "PREPARED")

        # Verify persisted JSON file
        task_file = TASKS_DATA_DIR / f"{task['task_id']}.json"
        self.assertTrue(task_file.exists())

        # Cleanup
        task_file.unlink(missing_ok=True)

    def test_03_submit_and_verify_task(self):
        """Verify task submission and automated verification test execution."""
        task = self.bridge.prepare_development_task(
            objective="Self Verification Test",
            problem_statement="Test verification pipeline",
            expected_behavior="Runs python unit tests and validates result",
            required_tests=["python -c \"print('Verification Passed')\""]
        )

        sub_res = self.bridge.submit_development_task(task)
        self.assertTrue(sub_res["success"])
        self.assertEqual(sub_res["status"], "SUBMITTED")

        ver_res = self.bridge.verify_development_changes(task["task_id"])
        self.assertTrue(ver_res["success"])
        self.assertTrue(ver_res["all_tests_passed"])

        # Cleanup
        task_file = TASKS_DATA_DIR / f"{task['task_id']}.json"
        task_file.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
