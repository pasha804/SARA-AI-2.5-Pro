# -*- coding: utf-8 -*-
"""
Automated unit tests for SARA's Project Discovery & Health Management subsystem.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

from sara_project_manager import ProjectManager, WORKSPACE_ROOT


class TestProjectManager(unittest.TestCase):

    def setUp(self):
        self.pm = ProjectManager(roots=[WORKSPACE_ROOT])

    def test_01_discover_projects(self):
        """Verify project scanner finds projects in workspace."""
        res = self.pm.discover_projects()
        self.assertTrue(res["success"])
        self.assertGreaterEqual(res["total_discovered"], 1)

    def test_02_audit_project_health(self):
        """Verify project health auditor returns health scores and issues breakdown."""
        projects = self.pm.discover_projects()["projects"]
        target_name = list(projects.keys())[0]

        audit = self.pm.audit_project(target_name)
        self.assertTrue(audit["success"])
        self.assertIn("health_score", audit)
        self.assertIn("status", audit)
        self.assertIn("checks_passed", audit)
        self.assertGreaterEqual(audit["health_score"], 0)
        self.assertLessEqual(audit["health_score"], 100)


if __name__ == "__main__":
    unittest.main()
