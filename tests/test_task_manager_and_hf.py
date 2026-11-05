# -*- coding: utf-8 -*-
"""
Tests for Background Task Manager (Phase 4) and Hugging Face Provider Adapter (Phase 8).
"""

import os
import time
import uuid
import unittest
from pathlib import Path
from sara_task_manager import BackgroundTaskManager
from sara_hf_provider import HuggingFaceProvider


class TestTaskManagerAndHF(unittest.TestCase):

    def setUp(self):
        self.test_db = Path(f"data/test_tasks_{uuid.uuid4().hex[:6]}.json")
        self.tm = BackgroundTaskManager(db_file=self.test_db, max_workers=2)

    def tearDown(self):
        self.tm.executor.shutdown(wait=False)
        if self.test_db.exists():
            for _ in range(3):
                try:
                    self.test_db.unlink()
                    break
                except Exception:
                    time.sleep(0.05)

    def test_task_creation_and_completion(self):
        task = self.tm.create_task("Compile Assets", "build_assets", {"target": "hud"}, timeout_seconds=5)
        self.assertIsNotNone(task.id)
        # Wait for task completion
        for _ in range(20):
            time.sleep(0.1)
            updated = self.tm.get_task(task.id)
            if updated and updated["status"] == "COMPLETED":
                break
        updated = self.tm.get_task(task.id)
        self.assertEqual(updated["status"], "COMPLETED")
        self.assertEqual(updated["progress"], 100)

    def test_duplicate_task_suppression(self):
        t1 = self.tm.create_task("Render 3D", "render", {"scene": "intro"}, timeout_seconds=10)
        t2 = self.tm.create_task("Render 3D", "render", {"scene": "intro"}, timeout_seconds=10)
        self.assertEqual(t1.id, t2.id)

    def test_pause_and_resume_task(self):
        task = self.tm.create_task("Heavy Computation", "compute", {"n": 1000}, auto_start=False)
        self.assertEqual(task.status, "QUEUED")
        self.assertTrue(self.tm.pause_task(task.id))
        self.assertEqual(self.tm.get_task(task.id)["status"], "PAUSED")
        self.assertTrue(self.tm.resume_task(task.id))
        self.assertIn(self.tm.get_task(task.id)["status"], ["QUEUED", "RUNNING"])

    def test_cancel_task(self):
        task = self.tm.create_task("Long Job", "long_job", {"duration": 60}, auto_start=False)
        self.assertTrue(self.tm.cancel_task(task.id))
        self.assertEqual(self.tm.get_task(task.id)["status"], "CANCELLED")

    def test_huggingface_adapter_defaults_and_fallback(self):
        provider = HuggingFaceProvider(api_token="test_mock_token")
        self.assertTrue(provider.is_configured())
        models = provider.get_supported_models()
        self.assertIn("qwen-coder-32b", models)
        self.assertIn("llama-3.3-70b", models)
        self.assertIn("deepseek-r1-32b", models)

    def test_huggingface_unconfigured_fallback(self):
        provider = HuggingFaceProvider(api_token="")
        self.assertFalse(provider.is_configured())
        res = provider.generate_chat([{"role": "user", "content": "hello"}])
        self.assertFalse(res["success"])
        self.assertTrue(res.get("fallback_recommended", False))


if __name__ == "__main__":
    unittest.main()
