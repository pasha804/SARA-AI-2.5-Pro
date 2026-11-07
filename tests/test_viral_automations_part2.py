# -*- coding: utf-8 -*-
"""
Tests for SARA AI 2.5 Pro — Viral Automations Part 2 (Batch 2)
Verifying:
  1. ClaudeMemAssociativeEngine (#9 Claude-Mem)
  2. BeadsWorkflowDAGOrchestrator (#22 Beads)
  3. ClaudeCodeRouterEngine (#27 Claude-Code-Router)
  4. TasteSkillAestheticLinter (#11 Taste-Skill, #12 UI-UX-Pro-Max)
  5. ClaudeLiveHUDTelemetry (#29 Claude-HUD)
  6. CcSwitchProfileManager (#28 CC-Switch)
"""

import unittest
from pathlib import Path
import json
import shutil

BASE_DIR = Path(r"D:\MARAA AI").resolve()
DATA_DIR = BASE_DIR / "data"

class TestViralAutomationsPart2(unittest.TestCase):

    def setUp(self):
        from sara_viral_automations_part2 import (
            ClaudeMemAssociativeEngine,
            BeadsWorkflowDAGOrchestrator,
            ClaudeCodeRouterEngine,
            TasteSkillAestheticLinter,
            ClaudeLiveHUDTelemetry,
            CcSwitchProfileManager
        )
        self.mem_engine = ClaudeMemAssociativeEngine()
        self.beads_engine = BeadsWorkflowDAGOrchestrator()
        self.router_engine = ClaudeCodeRouterEngine()
        self.taste_linter = TasteSkillAestheticLinter()
        self.hud_engine = ClaudeLiveHUDTelemetry()
        self.switch_manager = CcSwitchProfileManager()

    def test_claude_mem_associative_recall(self):
        # Store facts
        res = self.mem_engine.distill_and_store_turn(
            user_prompt="I am building SARA AI as a venture startup for Muhammad Mubashar (Pasha Dev)",
            assistant_reply="Understood Pasha Jan, SARA AI 2.5 Pro is locked and optimized for Pasha Dev with Discord NEXORA integration.",
            tags=["identity", "startup", "founder"],
            importance=5
        )
        self.assertTrue(res["success"])
        self.assertGreater(res["memory_count"], 0)

        # Associative Recall
        recalled = self.mem_engine.associative_recall("Who is the founder of SARA?", top_k=3)
        self.assertIsInstance(recalled, list)
        self.assertGreater(len(recalled), 0)
        self.assertIn("Pasha Dev", recalled[0]["content"])

        # Prompt Injection
        header = self.mem_engine.generate_prompt_memory_injection("Tell me about the venture startup")
        self.assertIn("SARA Active Recall Context", header)
        self.assertIn("Pasha Dev", header)

    def test_beads_workflow_dag_orchestrator(self):
        pipeline_id = "test_startup_flow"
        # Register a simple 3-bead DAG
        beads = [
            {
                "id": "step_extract",
                "name": "Extract Requirements",
                "action": "custom",
                "params": {"data": "startup_pitch"},
                "dependencies": []
            },
            {
                "id": "step_deck",
                "name": "Generate Deck Concept",
                "action": "custom",
                "params": {"slides": 5},
                "dependencies": ["step_extract"]
            },
            {
                "id": "step_notify",
                "name": "Notify Pasha",
                "action": "custom",
                "params": {"channel": "NEXORA"},
                "dependencies": ["step_deck"]
            }
        ]
        self.beads_engine.create_pipeline(pipeline_id, beads)
        
        # Execute pipeline
        result = self.beads_engine.execute_pipeline(pipeline_id, initial_context={"user": "Pasha Dev"})
        self.assertTrue(result["success"])
        self.assertEqual(result["completed_beads_count"], 3)
        self.assertEqual(result["failed_beads_count"], 0)
        self.assertIn("step_notify", result["results"])

    def test_claude_code_router(self):
        # 1. Simple task -> Local / Fast
        route_simple = self.router_engine.route_request("list files in current directory")
        self.assertEqual(route_simple["tier"], "TIER_FAST_LOCAL")

        # 2. Casual Voice / Chat -> Speed Flash
        route_chat = self.router_engine.route_request("kasa ho jani kya haal hain")
        self.assertEqual(route_chat["tier"], "TIER_SPEED_FLASH")

        # 3. Complex Architecture / Deep Refactoring -> Deep Reasoning Pro
        route_deep = self.router_engine.route_request("Refactor the entire neural dispatch pipeline with AST tree parsing and strict TDD")
        self.assertEqual(route_deep["tier"], "TIER_DEEP_REASONING_PRO")

        # 4. Multi-step goal -> Autonomous Manus
        route_manus = self.router_engine.route_request("Goal: Conduct deep market research on top 10 AI startups, create an executive Word doc and PowerPoint pitch deck")
        self.assertEqual(route_manus["tier"], "TIER_AUTONOMOUS_MANUS")

    def test_taste_skill_aesthetic_linter(self):
        # Sloppy code
        sloppy_html = """
        <div style="background: linear-gradient(135deg, #6366f1, #a855f7); border-radius: 12px; padding: 20px;">
            <div class="blob" style="filter: blur(40px); background: #ff007f;"></div>
            <h1>Unleash the power of AI</h1>
            <p>Our next-gen AI solution will revolutionize your workflow.</p>
            <button style="background: #6366f1; color: white;">Click Me</button>
        </div>
        """
        audit = self.taste_linter.audit_code(sloppy_html, file_type="html")
        self.assertFalse(audit["is_clean"])
        self.assertLess(audit["taste_score"], 60)
        self.assertGreater(len(audit["violations"]), 0)

        # Luxury Design Patch
        patch = self.taste_linter.generate_luxury_design_system_patch()
        self.assertIn(":root", patch)
        self.assertIn("--bg-primary", patch)
        self.assertIn("spring", patch)

    def test_claude_live_hud_telemetry(self):
        snapshot = self.hud_engine.get_telemetry_snapshot()
        self.assertIn("system_health", snapshot)
        self.assertIn("authorized_user", snapshot)
        self.assertEqual(snapshot["authorized_user"], "Muhammad Mubashar (Pasha Dev)")
        self.assertEqual(snapshot["discord_server"], "NEXORA")

        # ASCII HUD
        ascii_hud = self.hud_engine.render_terminal_hud()
        self.assertIn("SARA AI 2.5 PRO", ascii_hud)
        self.assertIn("TELEMETRY HUD", ascii_hud)

        # HTML Live HUD
        html_path = self.hud_engine.generate_live_html_hud()
        self.assertTrue(html_path.exists())
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            self.assertIn("SARA AI 2.5 Pro — Live Telemetry HUD", html_content)

    def test_cc_switch_profile_manager(self):
        profiles = self.switch_manager.list_profiles()
        self.assertGreaterEqual(len(profiles), 4)

        # Switch to founder
        f_res = self.switch_manager.switch_profile("founder")
        self.assertTrue(f_res["success"])
        self.assertEqual(self.switch_manager.get_active_profile()["id"], "founder")
        self.assertIn("Venture Founder", self.switch_manager.get_system_prompt_modifier())

        # Switch to dev_beast
        d_res = self.switch_manager.switch_profile("dev_beast")
        self.assertTrue(d_res["success"])
        self.assertEqual(self.switch_manager.get_active_profile()["id"], "dev_beast")
        self.assertIn("TDD", self.switch_manager.get_system_prompt_modifier())


if __name__ == "__main__":
    unittest.main()
