# -*- coding: utf-8 -*-
"""
Tests for SARA AI 2.5 Pro Full Automation & Skills Integration:
1. Semantic memory indexing & FTS5 search
2. WhatsApp Pakistani phone number standardizing (+923332656733)
3. browser-use autonomous engine import & execution
4. OpenViking multimodal context architecture
"""

import os
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from sara_memory_engine import memory_engine
from sara_neural_brain import whatsapp_open_chat


class TestFullAutomationAndSkills(unittest.TestCase):

    def test_01_sqlite_fts5_memory_engine(self):
        """Verifies semantic interaction logging and fast full-text search."""
        memory_engine.remember_fact("preferences", "Pasha Dev requested full desktop automation with browser-use and WhatsApp.")
        results = memory_engine.search_memory("desktop automation")
        self.assertTrue(len(results) > 0, "FTS5 memory search should return at least 1 match")
        matches = [r.get("content", "") for r in results]
        self.assertTrue(any("desktop automation" in m.lower() for m in matches))

    def test_02_whatsapp_pakistan_phone_formatting(self):
        """Verifies Pakistani local phone numbers are formatted to international WhatsApp standard without launching popups."""
        with patch("os.system") as mock_os_system:
            res = whatsapp_open_chat("03332656733", "Testing SARA WhatsApp Engine")
            self.assertTrue(res.get("success"), "WhatsApp open chat should succeed")
            self.assertEqual(res.get("action"), "sent_direct_phone")
            self.assertEqual(res.get("target"), "923332656733", "Local 0333... should be converted to 923332656733")
            mock_os_system.assert_called_once()

    def test_03_browser_use_engine_import(self):
        """Verifies browser-use repository is importable and ready for autonomous web tasks."""
        repo_dir = Path(__file__).resolve().parent.parent / "repositories" / "browser-use"
        if str(repo_dir) not in sys.path:
            sys.path.insert(0, str(repo_dir))
        try:
            import browser_use
            imported = True
        except Exception:
            imported = False
        self.assertTrue(imported, "browser_use module should be importable from repositories")

    def test_04_openviking_context_import(self):
        """Verifies OpenViking multimodal context module is importable."""
        repo_dir = Path(__file__).resolve().parent.parent / "repositories" / "OpenViking-main"
        if str(repo_dir) not in sys.path:
            sys.path.insert(0, str(repo_dir))
        try:
            import openviking
            imported = True
        except Exception:
            imported = False
        self.assertTrue(imported, "openviking package should be importable from repositories")


if __name__ == "__main__":
    unittest.main()
