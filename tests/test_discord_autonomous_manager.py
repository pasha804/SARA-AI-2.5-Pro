"""
SARA AI 2.5 — DISCORD AUTONOMOUS INTELLIGENCE TEST SUITE
Verifies:
  1. Strict NEXORA server lock and security enforcement
  2. 8 categories and 48 channels tree resolution
  3. Distinction between text channels, voice channels, and categories
  4. Channel name aliasing (general -> -general-chat, ai -> -ai-ml)
  5. Simulated sandbox message posting and engagement routine execution
"""

import sys
import unittest
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sara_automation_suite import DiscordAutonomousManager


class TestDiscordAutonomousManager(unittest.TestCase):

    def setUp(self):
        self.discord_mgr = DiscordAutonomousManager()

    def test_strict_server_security_guard(self):
        """Verifies that non-NEXORA servers are strictly blocked by security policy."""
        # NEXORA allowed
        self.assertTrue(self.discord_mgr.validate_server_target("NEXORA"))
        self.assertTrue(self.discord_mgr.validate_server_target("nexora"))
        self.assertTrue(self.discord_mgr.validate_server_target(""))  # Default

        # External server blocked
        self.assertFalse(self.discord_mgr.validate_server_target("HACKERS_GUILD"))
        self.assertFalse(self.discord_mgr.validate_server_target("RANDOM_SERVER"))

        # Blocked attempt returns error envelope
        res = self.discord_mgr.send_channel_message(
            target="-general-chat",
            message="Test",
            server_name="EXTERNAL_SERVER",
            simulate=True
        )
        self.assertFalse(res["success"])
        self.assertIn("Security Guard", res["error"])

    def test_category_and_channel_tree_structure(self):
        """Validates all 8 categories and 59 total channels in NEXORA server topology."""
        tree = self.discord_mgr.list_server_channels()
        self.assertEqual(tree["server"], "NEXORA")
        self.assertEqual(tree["categories_count"], 8)
        self.assertEqual(tree["total_channels"], 59)

        expected_categories = [
            "VOICE CHANNELS",
            "INFORMATION",
            "COMMUNITY",
            "DEVELOPMENT",
            "PROJECTS",
            "COLLABORATION",
            "LEARNING HUB",
            "CAREERS"
        ]
        for cat in expected_categories:
            self.assertIn(cat, tree["categories"])

    def test_channel_resolution_and_aliases(self):
        """Tests that aliases and partial names resolve to exact NEXORA channel names."""
        # General chat alias
        dist_gen = self.discord_mgr.distinguish_channel("general")
        self.assertFalse(dist_gen["is_category"])
        self.assertEqual(dist_gen["channel"], "-general-chat")
        self.assertEqual(dist_gen["type"], "text")

        # Python channel
        dist_py = self.discord_mgr.distinguish_channel("python")
        self.assertEqual(dist_py["channel"], "-python")
        self.assertEqual(dist_py["category"], "DEVELOPMENT")
        self.assertEqual(dist_py["prefix"], "🐍")

        # Voice channel
        dist_vc = self.discord_mgr.distinguish_channel("General VC")
        self.assertEqual(dist_vc["type"], "voice")
        self.assertEqual(dist_vc["category"], "VOICE CHANNELS")

        # Category resolution
        dist_cat = self.discord_mgr.distinguish_channel("CAREERS")
        self.assertTrue(dist_cat["is_category"])
        self.assertEqual(dist_cat["category"], "CAREERS")
        self.assertEqual(len(dist_cat["channels"]), 6)

    def test_simulated_message_dispatch(self):
        """Verifies simulated sandbox message dispatching without desktop side effects."""
        res = self.discord_mgr.send_channel_message(
            target="general",
            message="Salam Pasha Jan! SARA autonomous Discord intelligence is verified.",
            server_name="NEXORA",
            simulate=True
        )
        self.assertTrue(res["success"])
        self.assertTrue(res["simulated"])
        self.assertEqual(res["target"], "-general-chat")
        self.assertEqual(res["server"], "NEXORA")


if __name__ == "__main__":
    unittest.main()
