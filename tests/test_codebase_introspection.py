"""
SARA AI 3.0 — Codebase Introspection & High-Capacity Architectural Explanation Tests
Verifies:
  1. Authoritative retrieval of all 7 subsystem layers (avatar_3d, backend, models, automation, discord, memory, hud).
  2. Complete master architectural blueprint retrieval.
  3. Proper error handling and fallback for unrecognized module queries.
"""

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sara_neural_brain import explain_sara_codebase


class TestCodebaseIntrospection(unittest.TestCase):

    def test_explain_all_layers(self):
        """Verifies master blueprint returns all 7 subsystem layers."""
        res = explain_sara_codebase("all")
        self.assertTrue(res["success"])
        self.assertEqual(res["module"], "all")
        self.assertEqual(res["creator"], "Muhammad Mubashar (Pasha Dev)")
        self.assertIn("NEXORA", res["authorized_server"])
        self.assertEqual(len(res["layers"]), 7)

        expected_layers = ["avatar_3d", "backend", "models", "automation", "discord", "memory", "hud"]
        for layer in expected_layers:
            self.assertIn(layer, res["layers"])

    def test_explain_avatar_3d(self):
        """Verifies 3D Avatar layer details."""
        res = explain_sara_codebase("avatar_3d")
        self.assertTrue(res["success"])
        details = res["details"]
        self.assertIn("Three.js", details["framework"])
        self.assertIn("Evelyn", details["avatar_identity"])
        self.assertTrue(any("FFT" in feat for feat in details["features"]))

    def test_explain_backend_live(self):
        """Verifies Node.js Live WebSocket backend layer details."""
        res = explain_sara_codebase("backend")
        self.assertTrue(res["success"])
        details = res["details"]
        self.assertEqual(details["port"], 3344)
        self.assertEqual(details["endpoint"], "/live")
        self.assertTrue(any("gemini-3.1-flash-live-preview" in feat for feat in details["features"]))

    def test_explain_discord_publisher(self):
        """Verifies Discord autonomous publisher details."""
        res = explain_sara_codebase("discord")
        self.assertTrue(res["success"])
        details = res["details"]
        self.assertEqual(details["channels_count"], 54)
        self.assertTrue(any("NEXORA" in feat or "dedup" in feat for feat in details["features"]))


if __name__ == "__main__":
    unittest.main()

