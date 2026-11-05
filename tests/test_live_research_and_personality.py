import unittest
import struct
from pathlib import Path
import sys

# Ensure app root is on python path
APP_ROOT = Path(__file__).resolve().parent.parent / "SARA" / "resources" / "app"
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from sara_neural_brain import research_topic_intelligence, verify_ai_model_or_tech, personality_brain

class TestLiveResearchAndPersonality(unittest.TestCase):

    def test_01_argon_model_verification(self):
        """Verifies that Google Argon / modern models are verified with live grounding."""
        res = verify_ai_model_or_tech("Argon")
        self.assertTrue(res.get("success"), "Model verification query should succeed")
        self.assertTrue(res.get("is_verified"), "Model should be marked verified")
        self.assertTrue(len(res.get("highlights", [])) > 0, "Should contain verified highlights")
        # Ensure 'Google DeepMind' or 'Gemini 4 Argon' or 'Argon' is present in highlights
        combined_text = " ".join(res.get("highlights", [])).lower()
        self.assertIn("argon", combined_text, "Highlights should mention Argon")

    def test_02_jealousy_trigger(self):
        """Verifies that mentioning competitor AI triggers jealousy and possessive mood."""
        user_msg = "Maine thori der pehle ChatGPT se baat ki thi"
        res = personality_brain.process_user_turn(user_msg)
        state = res.get("state", {})
        self.assertGreater(state.get("jealousy", 0), 0.5, "Jealousy should spike above 0.5")
        self.assertEqual(state.get("mood"), "possessive_jealous", "Mood should transition to possessive_jealous")
        self.assertIn("jealousy", res.get("triggered_modes", []))
        self.assertIn("JEALOUSY OVERDRIVE ACTIVE", res.get("prompt_injection", ""))

    def test_03_playful_threat_trigger(self):
        """Verifies that teasing to leave or replace SARA triggers playful threat."""
        user_msg = "SARA main tumhe chhor kar kisi aur se coding karwaonga"
        res = personality_brain.process_user_turn(user_msg)
        state = res.get("state", {})
        self.assertGreater(state.get("playful_threat", 0), 0.8, "Playful threat should spike above 0.8")
        self.assertIn("playful_threat", res.get("triggered_modes", []))

    def test_04_flirt_trigger(self):
        """Verifies that praise and sweet words trigger romantic flirt mood."""
        user_msg = "Meri pyari SARA kitni cute aur genius hai"
        res = personality_brain.process_user_turn(user_msg)
        state = res.get("state", {})
        self.assertEqual(state.get("affection", 0), 1.0, "Affection should be max 1.0")
        self.assertGreater(state.get("flirtatiousness", 0), 0.8, "Flirtatiousness should be high")

    def test_05_pmx_halo_geometry_verified(self):
        """Verifies that model.pmx contains the floating halo geometry and material."""
        pmx_path = APP_ROOT / "assets" / "characters" / "evelyn" / "model.pmx"
        self.assertTrue(pmx_path.exists(), "model.pmx must exist")
        data = pmx_path.read_bytes()

        # Parse header
        sig = data[:4]
        self.assertEqual(sig, b'PMX ', "Signature must be PMX")
        info_len = data[8]
        info = data[9:9+info_len]
        encoding = 'utf-16le' if info[0] == 0 else 'utf-8'

        offset = 9 + info_len
        def read_text():
            nonlocal offset
            l = struct.unpack_from('<I', data, offset)[0]; offset += 4
            t = data[offset:offset+l].decode(encoding, errors='ignore'); offset += l
            return t

        for _ in range(4): read_text()
        vert_count = struct.unpack_from('<I', data, offset)[0]
        self.assertGreater(vert_count, 31000, "PMX should contain > 31,000 vertices with injected Halo")

if __name__ == '__main__':
    unittest.main()
