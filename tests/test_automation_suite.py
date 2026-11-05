# -*- coding: utf-8 -*-
"""
Tests for SARA AI 2.5 Pro — Unified n8n Autonomous Automation Suite
Validates all 5 integrated pipelines end-to-end:
  1. WhatsApp Lead Qualification & CRM Sync
  2. Deep Web Research Crawler
  3. Study Notes & PDF Tutor Engine
  4. Email & Notification Digest
  5. Multi-channel Social & Discord Publisher
"""

import os
import sys
import json
import unittest
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(r"D:\MARAA AI").resolve()
sys.path.insert(0, str(BASE_DIR))

from sara_automation_suite import (
    whatsapp_smart_pipeline,
    deep_research_crawler,
    study_notes_pdf_tutor,
    email_notification_digest,
    social_discord_publisher
)


class TestSARAAutomationSuite(unittest.TestCase):

    def test_pipeline_1_whatsapp_lead_qualification(self):
        """Test WhatsApp message analysis, lead categorization, and auto-reply draft."""
        res = whatsapp_smart_pipeline.qualify_and_route_lead(
            contact_name="Farhan Tech",
            message="Hey Pasha, we need an automated trading dashboard developed. What is your rate and timeline?",
            phone="+923332656733"
        )
        self.assertTrue(res.get("success"))
        self.assertEqual(res.get("intent"), "sales_lead")
        self.assertEqual(res.get("urgency"), "high")
        self.assertIn("Mubashar (Pasha Dev)", res.get("suggested_reply"))
        self.assertIn("Pasha Jan", res.get("spoken_alert"))

    def test_pipeline_2_deep_research_crawler(self):
        """Test deep web scraping, HTML cleaning, and key highlights extraction."""
        res = deep_research_crawler.crawl_url("https://example.com")
        self.assertTrue(res.get("success"))
        self.assertIn("Example Domain", res.get("title"))
        self.assertIsInstance(res.get("highlights"), list)
        self.assertTrue(len(res.get("highlights")) > 0)
        self.assertIn("Pasha Jan", res.get("spoken_reply"))

    def test_pipeline_3_study_notes_and_pdf_tutor(self):
        """Test academic document parsing, concept breakdown, and quiz deck generation."""
        doc_path = str(BASE_DIR / "architecture.md")
        res = study_notes_pdf_tutor.generate_study_pack(doc_path, "System Architecture Review")
        self.assertTrue(res.get("success"))
        self.assertGreater(res.get("concepts_count"), 0)
        self.assertGreater(res.get("quiz_count"), 0)
        pack = res.get("study_pack", {})
        self.assertIn("quiz_questions", pack)
        first_q = pack["quiz_questions"][0]
        self.assertIn("question", first_q)
        self.assertEqual(len(first_q["options"]), 4)

    def test_pipeline_4_email_notification_digest(self):
        """Test daily notification briefing generation and spoken summary."""
        res = email_notification_digest.generate_spoken_briefing()
        self.assertTrue(res.get("success"))
        digest = res.get("digest", {})
        self.assertGreater(digest.get("total_count"), 0)
        self.assertIn("Pasha Jan", res.get("spoken_reply"))
        self.assertIsInstance(digest.get("highlights"), list)

    def test_pipeline_5_social_media_discord_publisher(self):
        """Test multi-channel content formatting for Discord, Twitter, and LinkedIn."""
        res = social_discord_publisher.create_multichannel_post(
            title="SARA Neural Companion 2.5",
            description="Autonomous desktop companion equipped with real-time vision, voice, and automated task execution."
        )
        self.assertTrue(res.get("success"))
        pack = res.get("pack", {})
        self.assertIn("discord", pack)
        self.assertIn("twitter", pack)
        self.assertIn("linkedin", pack)
        self.assertIn("🚀 **SARA Neural Companion 2.5**", pack["discord"])
        self.assertIn("Pasha Jan", res.get("spoken_reply"))


if __name__ == "__main__":
    unittest.main()

