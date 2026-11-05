# -*- coding: utf-8 -*-
"""
Automated unit tests for SARA's Advanced Features:
- WhatsApp Voice Transcriber
- Wake-Word Detector
- Browser Deep-Dive Engine
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

from sara_whatsapp_voice import WhatsAppVoiceTranscriber
from sara_wakeword import SaraWakeWordDetector
from sara_browser_deepdive import BrowserDeepDive


class TestAdvancedFeatures(unittest.TestCase):

    def test_01_whatsapp_voice_transcriber_contract(self):
        """Verify WhatsApp voice transcriber returns valid schema even when no files are present."""
        transcriber = WhatsAppVoiceTranscriber()
        res = transcriber.transcribe_and_summarize("Furqan")
        self.assertTrue(res["success"])
        self.assertIn("spoken_reply", res)
        self.assertIn("summary", res)

    def test_02_wakeword_matching_and_response(self):
        """Verify wake-word detector triggers window restoration on matched keyword."""
        detector = SaraWakeWordDetector()
        res = detector.simulate_wake_word_trigger("Hey SARA Suno")
        self.assertTrue(res["success"])
        self.assertEqual(res["matched_keyword"], "hey sara suno")
        self.assertIn("spoken_reply", res)

    def test_03_browser_deepdive_script_generation(self):
        """Verify highlighter script contains styles and target terms."""
        deepdive = BrowserDeepDive()
        js_code = deepdive.generate_highlighter_js(["neural", "vision"])
        self.assertIn("sara-live-highlight", js_code)
        self.assertIn("neural", js_code)
        self.assertIn("vision", js_code)

    def test_04_trading_risk_calculation(self):
        """Verify Exness risk & lot size calculator returns accurate trade parameters."""
        sys.path.insert(0, str(Path(__file__).parent.parent.resolve() / "SARA" / "resources" / "app"))
        from sara_neural_brain import calculate_trading_risk
        res = calculate_trading_risk(balance_usd=1000.0, risk_percent=1.0, stop_loss_pips=20.0, pair="XAUUSD")
        self.assertTrue(res["success"])
        self.assertIn("lot_size", res)
        self.assertIn("spoken_reply", res)
        self.assertIn("hud_card", res)
        self.assertEqual(res["pair"], "XAUUSD")
        self.assertGreaterEqual(res["lot_size"], 0.01)


if __name__ == "__main__":
    unittest.main()
