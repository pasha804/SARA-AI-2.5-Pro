# -*- coding: utf-8 -*-
"""
SARA AI 2.5 Pro - Autonomous Expansion & Continuous Engineering Verification Suite
Tests memory profile synthesis, SQLite backup, NEXORA Discord channel distinction,
C: Drive cleanable space analysis, project scaffolding, and APInex working model alignment.
"""

import os
import sys
import json
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add workspace root to sys.path
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from sara_memory_engine import memory_engine
from sara_automation_suite import (
    discord_autonomous_manager,
    c_drive_cleaner,
    browser_first_link_manager,
    n8n_catalog
)
from sara_project_manager import project_manager
from sara_self_improvement import self_improvement


class TestAutonomousExpansion(unittest.TestCase):

    def test_01_user_profile_synthesis(self):
        """Test persistent memory profile synthesis accurately captures Pasha Jan's identity & credentials."""
        profile = memory_engine.synthesize_user_profile()
        self.assertIsInstance(profile, dict)
        self.assertEqual(profile.get("user_name"), "Pasha Jan")
        self.assertEqual(profile.get("email"), "pashadev804@gmail.com")
        self.assertEqual(profile.get("phone"), "+923332656733")
        self.assertEqual(profile.get("authorized_discord_server"), "NEXORA")
        self.assertIn("free/glm-5.3-flashx", profile.get("top_models", []))
        self.assertIn("free/gemini-3.8-flash", profile.get("top_models", []))
        self.assertIn("free/deepseek-v4-pro-0813", profile.get("top_models", []))

    def test_02_memory_backup(self):
        """Test persistent SQLite memory backup generation."""
        backup_res = memory_engine.backup_memory()
        self.assertTrue(backup_res.get("success"))
        backup_path = Path(backup_res.get("backup_path", ""))
        self.assertTrue(backup_path.exists())
        self.assertGreater(backup_path.stat().st_size, 0)

    def test_03_discord_distinguish_all_categories(self):
        """Test distinction between voice channels, text channels, and categories in NEXORA."""
        # Voice channels
        v1 = discord_autonomous_manager.distinguish_channel("General VC")
        self.assertEqual(v1.get("type"), "voice")
        self.assertEqual(v1.get("server"), "NEXORA")

        v2 = discord_autonomous_manager.distinguish_channel("study-room")
        self.assertEqual(v2.get("type"), "voice")
        self.assertEqual(v2.get("channel"), "-study-room")

        # Text channels
        t1 = discord_autonomous_manager.distinguish_channel("general")
        self.assertEqual(t1.get("type"), "text")
        self.assertEqual(t1.get("channel"), "-general-chat")

        t2 = discord_autonomous_manager.distinguish_channel("python")
        self.assertEqual(t2.get("type"), "text")
        self.assertEqual(t2.get("channel"), "-python")

        t3 = discord_autonomous_manager.distinguish_channel("ai-ml")
        self.assertEqual(t3.get("type"), "text")
        self.assertEqual(t3.get("channel"), "-ai-ml")

        # Categories
        cat = discord_autonomous_manager.distinguish_channel("DEVELOPMENT")
        self.assertTrue(cat.get("is_category"))
        self.assertIn("-python", cat.get("channels", []))
        self.assertIn("-backend", cat.get("channels", []))

    def test_04_discord_server_whitelist_guard(self):
        """Test security guard strictly rejects targeting any Discord server other than NEXORA."""
        res = discord_autonomous_manager.send_channel_message("general", "Hello", server_name="ForeignGuild")
        self.assertFalse(res.get("success"))
        self.assertIn("Security Guard", res.get("error", ""))

    def test_05_c_drive_disk_analysis(self):
        """Test C: Drive cleanable space analysis produces itemized safe cache breakdown."""
        report = c_drive_cleaner.analyze_cleanable_space(max_files_per_category=50)
        self.assertTrue(report.get("success"))
        self.assertIn("total_cleanable_gb", report)
        self.assertIn("categories", report)
        self.assertIn("spoken_summary", report)
        self.assertIn("Pasha Jan", report.get("spoken_summary", ""))

    def test_06_c_drive_clean_dry_run(self):
        """Test selective cache cleaning execution with dry_run simulation."""
        clean_res = c_drive_cleaner.clean_space(selected_keys=["npm_cache"], dry_run=True)
        self.assertTrue(clean_res.get("success"))
        self.assertIn("freed_mb", clean_res)

    def test_07_project_scaffolding_and_validation(self):
        """Test autonomous web dashboard scaffolding and error self-healing."""
        scaffold_res = project_manager.create_autonomous_project("pasha_nexus_dashboard", launch_antigravity=False)
        self.assertTrue(scaffold_res.get("success"))
        proj_path = Path(scaffold_res.get("project_path", ""))
        self.assertTrue((proj_path / "index.html").exists())
        self.assertTrue((proj_path / "src" / "styles.css").exists())

        # Test self-healing syntax audit
        healing_res = project_manager.resolve_project_errors(str(proj_path))
        self.assertTrue(healing_res.get("success"))
        self.assertEqual(healing_res.get("status"), "CLEAN")

    def test_08_n8n_catalog_scale(self):
        """Test n8n automations catalog contains 415 verified workflows across 25 categories."""
        cats = n8n_catalog.list_categories()
        self.assertEqual(cats.get("total_workflows"), 415)
        self.assertEqual(cats.get("total_categories"), 25)

        # Search verification
        discord_search = n8n_catalog.search_workflows("discord")
        self.assertGreater(discord_search.get("count", 0), 0)

    def test_09_top_working_models_in_env(self):
        """Verify .env strictly configures verified active APInex models and eradicates 402 models."""
        env_path = WORKSPACE_ROOT / ".env"
        self.assertTrue(env_path.exists())
        content = env_path.read_text(encoding="utf-8")
        self.assertIn("SARA_CHAT_MODEL=free/glm-5.3-flashx", content)
        self.assertIn("SARA_CODE_MODEL=free/deepseek-v4-pro-0813", content)
        self.assertIn("SARA_RESEARCH_MODEL=free/kimi-k3", content)
        self.assertNotIn("SARA_CHAT_MODEL=free/mimo-v2.6-pro", content)


if __name__ == "__main__":
    unittest.main()
