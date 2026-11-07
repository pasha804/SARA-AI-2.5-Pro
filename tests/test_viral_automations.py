# -*- coding: utf-8 -*-
import os
import sys
import unittest
from pathlib import Path

BASE_DIR = Path(r"D:\MARAA AI").resolve()
sys.path.insert(0, str(BASE_DIR))

from sara_advanced_viral_automations import (
    repomix_packer,
    firecrawl_crawler,
    vibe_kanban,
    headroom_guard,
    caveman_compressor,
    CODEBASE_PACKS_DIR,
    KANBAN_DIR
)


class TestAdvancedViralAutomations(unittest.TestCase):

    def test_repomix_packer(self):
        """Test packing repository files into token-optimized AI bundle."""
        res = repomix_packer.pack_repository(pack_name="unit_test_pack", max_files=5)
        self.assertTrue(res.get("success"))
        self.assertGreater(res.get("files_packed", 0), 0)
        self.assertGreater(res.get("estimated_tokens", 0), 0)
        self.assertTrue(Path(res.get("pack_file")).exists())
        self.assertIn("Pasha Jan", res.get("spoken_reply", ""))

    def test_vibe_kanban_workflow(self):
        """Test Kanban task creation, state transition, and HTML board rendering."""
        res_add = vibe_kanban.add_task(title="Unit Test Task", column="backlog", priority="HIGH")
        self.assertTrue(res_add.get("success"))
        task_id = res_add["task"]["id"]

        # Move to In Progress
        res_move = vibe_kanban.move_task(task_id, "in_progress")
        self.assertTrue(res_move.get("success"))
        self.assertEqual(res_move.get("moved_to"), "in_progress")
        self.assertTrue((KANBAN_DIR / "vibe_kanban_board.html").exists())

    def test_headroom_context_guard(self):
        """Test proactive headroom calculation and context window protection."""
        dialogue = [
            {"role": "user", "text": "Can you design a high-end agent architecture?"},
            {"role": "model", "text": "Certainly, let's architect a multi-tiered system."}
        ]
        res = headroom_guard.audit_and_compact(dialogue, model_limit_tokens=32000)
        self.assertTrue(res.get("success"))
        self.assertGreater(res.get("headroom_tokens", 0), 0)
        self.assertGreater(res.get("headroom_percent", 0), 50.0)

    def test_caveman_telegraphic_compression(self):
        """Test removing conversational fluff for low-latency execution."""
        fluff_text = "As an AI language model, I would be happy to help you in order to complete this task certainly."
        res = caveman_compressor.compress_telegraphic(fluff_text)
        self.assertTrue(res.get("success"))
        self.assertGreater(res.get("tokens_saved_percent", 0), 20.0)
        self.assertNotIn("as an ai language model", res.get("compressed_text", "").lower())


if __name__ == "__main__":
    unittest.main()
