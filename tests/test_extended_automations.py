# -*- coding: utf-8 -*-
import os
import sys
import unittest
from pathlib import Path

BASE_DIR = Path(r"D:\MARAA AI").resolve()
DATA_DIR = BASE_DIR / "data"
sys.path.insert(0, str(BASE_DIR))

from sara_automation_suite import (
    whatsapp_smart_pipeline,
    deep_research_crawler,
    study_notes_pdf_tutor,
    email_notification_digest,
    social_discord_publisher,
    discord_autonomous_manager,
    browser_first_link_manager,
    c_drive_cleaner,
    n8n_catalog,
    startup_pitch_deck_engine,
    client_outreach_engine,
    codebase_security_engine,
    startup_revenue_engine
)
from sara_project_manager import project_manager
from sara_self_improvement import self_improvement


class TestExtendedAutomationSuite(unittest.TestCase):

    def test_pipeline_6_discord_autonomous_manager(self):
        """Test Discord window detection and channel navigation command synthesis."""
        res = discord_autonomous_manager.focus_discord()
        self.assertTrue(res.get("success"))
        self.assertTrue("message" in res)

    def test_pipeline_7_browser_first_link_manager(self):
        """Test first search result URL extraction and execution."""
        res = browser_first_link_manager.open_first_link("FastAPI Python official documentation")
        self.assertTrue(res.get("success"))
        self.assertIn("url", res)
        self.assertIn("Pasha Jan", res.get("spoken_reply", ""))

    def test_pipeline_8_c_drive_cleaner_analysis(self):
        """Test C: drive expendable space analysis and spoken Urdu summary."""
        res = c_drive_cleaner.analyze_cleanable_space()
        self.assertTrue(res.get("success"))
        self.assertGreater(res.get("total_cleanable_mb", 0), 0)
        self.assertIn("categories", res)
        self.assertIn("Pasha Jan", res.get("spoken_summary", ""))

    def test_pipeline_9_n8n_catalog_and_search(self):
        """Test 360+ templates catalog, category indexing, and search capabilities."""
        summary = n8n_catalog.list_categories()
        self.assertTrue(summary.get("success"))
        self.assertGreaterEqual(summary.get("total_categories", 0), 20)
        self.assertGreaterEqual(summary.get("total_workflows", 0), 300)

        # Search discord workflows
        search_res = n8n_catalog.search_workflows("discord")
        self.assertTrue(search_res.get("success"))
        self.assertGreater(search_res.get("count", 0), 0)

        # Execute workflow
        exec_res = n8n_catalog.execute_workflow("Discord AI-powered bot")
        self.assertTrue(exec_res.get("success"))
        self.assertEqual(exec_res.get("status"), "COMPLETED")

    def test_autonomous_coding_and_project_scaffolding(self):
        """Test full-stack project creation, code generation, and test execution."""
        res = project_manager.create_autonomous_project(
            project_name="pasha_unit_test_proj",
            project_type="Automated Test Suite Web App",
            launch_antigravity=False
        )
        self.assertTrue(res.get("success"))
        self.assertEqual(res.get("audit", {}).get("health_score"), 100)
        self.assertEqual(res.get("diagnostics", {}).get("status"), "CLEAN")
        p_dir = Path(res.get("project_path"))
        self.assertTrue((p_dir / "index.html").exists())
        self.assertTrue((p_dir / "server.py").exists())
        self.assertTrue((p_dir / "package.json").exists())

    def test_self_improvement_evaluation(self):
        """Test self-improvement capabilities assessment."""
        res = self_improvement.evaluate_system_capabilities()
        self.assertEqual(res.get("overall_health"), "OPTIMAL")

    def test_pipeline_10_startup_pitch_deck_engine(self):
        """Test automated 10-slide VC pitch deck generation and markdown export."""
        res = startup_pitch_deck_engine.generate_pitch_deck()
        self.assertTrue(res.get("success"))
        self.assertEqual(res.get("total_slides"), 10)
        self.assertIn("Pasha Jan", res.get("spoken_pitch_ur", ""))
        self.assertTrue((DATA_DIR / "startup" / "pitch_deck_sara.json").exists())
        self.assertTrue((DATA_DIR / "startup" / "pitch_deck_sara.md").exists())

    def test_pipeline_11_client_outreach_engine(self):
        """Test B2B cold email, LinkedIn note, and WhatsApp voice script generation."""
        res = client_outreach_engine.create_campaign(
            lead_name="Sophia Vance",
            lead_company="Hyperion Ventures",
            lead_email="sophia@hyperion.ai"
        )
        self.assertTrue(res.get("success"))
        self.assertIn("sequences", res.get("campaign", {}))
        self.assertIn("email_touch_1", res["campaign"]["sequences"])
        self.assertIn("Pasha Jan", res.get("spoken_summary", ""))

    def test_pipeline_12_codebase_security_engine(self):
        """Test autonomous security audit and Executive Health Certificate."""
        res = codebase_security_engine.run_security_audit(max_files=50)
        self.assertTrue(res.get("success"))
        self.assertIn(res.get("security_grade"), ["A+", "A", "B"])
        self.assertGreaterEqual(res.get("security_score", 0), 70)
        self.assertTrue((DATA_DIR / "startup" / "security_audit_certificate.json").exists())

    def test_pipeline_13_startup_revenue_engine(self):
        """Test MRR, ARR, LTV:CAC, runway and SaaS valuation simulation."""
        res = startup_revenue_engine.simulate_financials(active_subscribers=100, avg_price_per_month=49.0)
        self.assertTrue(res.get("success"))
        self.assertEqual(res.get("active_subscribers"), 100)
        self.assertGreater(res.get("mrr", 0), 0)
        self.assertGreater(res.get("arr", 0), 0)
        self.assertTrue(res.get("is_profitable"))
        self.assertIn("Pasha Jan", res.get("spoken_summary", ""))


if __name__ == "__main__":
    unittest.main()
