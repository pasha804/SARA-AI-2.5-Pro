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

    def test_dynamic_daily_topic_relevance(self):
        """Verifies that each channel produces specialized, topic-relevant daily content."""
        # Python
        msg_py = self.discord_mgr.generate_daily_message("python")
        self.assertTrue(any(kw in msg_py for kw in ["Python", "uv", "typing", "match/case", "pathlib"]))
        self.assertIn("NEXORA", msg_py)

        # React
        msg_react = self.discord_mgr.generate_daily_message("react")
        self.assertTrue(any(kw in msg_react for kw in ["React", "useMemo", "motion", "Server Actions"]))

        # Cybersecurity
        msg_sec = self.discord_mgr.generate_daily_message("cybersecurity")
        self.assertTrue(any(kw in msg_sec for kw in ["Security", "CSP", "Argon2", "TruffleHog"]))

        # Daily Wins
        msg_wins = self.discord_mgr.generate_daily_message("daily-wins")
        self.assertTrue(any(kw in msg_wins for kw in ["Win", "Celebrate", "Progress", "accomplishment"]))

    def test_daily_message_cross_date_uniqueness(self):
        """Ensures that messages across consecutive days rotate and do not repeat."""
        import datetime
        d1 = datetime.date(2026, 11, 9)
        d2 = datetime.date(2026, 11, 10)
        msg1 = self.discord_mgr.generate_daily_message("python", date_obj=d1)
        msg2 = self.discord_mgr.generate_daily_message("python", date_obj=d2)
        self.assertNotEqual(msg1, msg2)

    def test_run_daily_all_channels_engagement_simulated(self):
        """Verifies full batch execution across all 54 text channels on NEXORA."""
        res = self.discord_mgr.run_daily_all_channels_engagement(simulate=True, force=True)
        self.assertTrue(res["success"])
        self.assertEqual(res["server"], "NEXORA")
        self.assertEqual(res["total_channels"], 54)
        self.assertEqual(res["posted_count"], 54)
        self.assertEqual(res["failed_count"], 0)
        self.assertIn("54 channels", res["spoken_reply"])

    def test_deduplication_ledger_skips_duplicates(self):
        """Ensures that duplicate posts on the same date are skipped unless force=True."""
        # First post succeeds
        res1 = self.discord_mgr.post_daily_to_channel("python", simulate=True, force=True)
        self.assertTrue(res1["success"])
        self.assertFalse(res1["skipped"])

        # Second post on same day without force is skipped
        res2 = self.discord_mgr.post_daily_to_channel("python", simulate=True, force=False)
        self.assertTrue(res2["success"])
        self.assertTrue(res2["skipped"])
        self.assertIn("Already posted", res2["reason"])


if __name__ == "__main__":
    unittest.main()
