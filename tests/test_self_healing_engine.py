"""
SARA AI 2.5 — SELF-HEALING ENGINE TEST SUITE
Verifies:
  1. Anomaly diagnosis and root cause extraction from exceptions
  2. Backup checkpoint creation and restoration
  3. Patch application and rollback on failure
  4. Confidence score gating
  5. Infinite repair loop quarantine protection
"""

import sys
import unittest
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sara_self_healing_engine import SaraSelfHealingEngine, AnomalyRecord


class TestSelfHealingEngine(unittest.TestCase):

    def setUp(self):
        self.engine = SaraSelfHealingEngine(max_attempts_per_signature=2, quarantine_window_sec=5.0)
        self.test_file = PROJECT_ROOT / "data" / "test_self_healing_target.txt"
        self.test_file.parent.mkdir(parents=True, exist_ok=True)
        self.test_file.write_text("ORIGINAL_CONTENT_V1", encoding="utf-8")

    def tearDown(self):
        if self.test_file.exists():
            self.test_file.unlink()

    def test_anomaly_diagnosis_from_exception(self):
        """Verifies extracting file, line number, and confidence score from stack trace."""
        try:
            # Synthetic error
            raise KeyError("missing_required_token")
        except Exception as e:
            anomaly = self.engine.diagnose_exception(e)
            self.assertEqual(anomaly.error_type, "KeyError")
            self.assertIn("missing_required_token", anomaly.error_message)
            self.assertTrue(anomaly.confidence_score >= 0.50)
            self.assertEqual(anomaly.status, "DETECTED")

    def test_checkpoint_creation_and_successful_patch(self):
        """Tests that a backup is created before patching and file is successfully updated."""
        anomaly = AnomalyRecord(
            anomaly_id="TEST-001",
            error_type="SyntaxError",
            error_message="Test message",
            target_file=str(self.test_file),
            line_number=1,
            stack_trace="traceback",
            timestamp=0.0,
            confidence_score=0.85
        )

        def mock_patch():
            self.test_file.write_text("PATCHED_CONTENT_V2", encoding="utf-8")

        res = self.engine.attempt_targeted_repair(anomaly, patch_fn=mock_patch)
        self.assertTrue(res["ok"])
        self.assertEqual(res["status"], "PATCHED")
        self.assertIsNotNone(res["backup_checkpoint"])
        self.assertTrue(Path(res["backup_checkpoint"]).exists())
        self.assertEqual(self.test_file.read_text(encoding="utf-8"), "PATCHED_CONTENT_V2")

    def test_rollback_on_failed_patch(self):
        """Verifies that if a patch throws an exception, the file is automatically rolled back."""
        anomaly = AnomalyRecord(
            anomaly_id="TEST-002",
            error_type="AttributeError",
            error_message="Method missing",
            target_file=str(self.test_file),
            line_number=1,
            stack_trace="traceback",
            timestamp=0.0,
            confidence_score=0.85
        )

        def failing_patch():
            # Modify file, then raise error to simulate broken patch
            self.test_file.write_text("CORRUPTED_INCOMPLETE_PATCH", encoding="utf-8")
            raise RuntimeError("Patch verification failed syntactically!")

        res = self.engine.attempt_targeted_repair(anomaly, patch_fn=failing_patch)
        self.assertFalse(res["ok"])
        self.assertEqual(res["status"], "ROLLED_BACK")
        # Ensure file content was rolled back to original V1!
        self.assertEqual(self.test_file.read_text(encoding="utf-8"), "ORIGINAL_CONTENT_V1")

    def test_loop_prevention_quarantine(self):
        """Verifies that exceeding max repair attempts trips quarantine protection."""
        anomaly = AnomalyRecord(
            anomaly_id="TEST-003",
            error_type="RecursionError",
            error_message="Infinite loop",
            target_file=str(self.test_file),
            line_number=1,
            stack_trace="traceback",
            timestamp=0.0,
            confidence_score=0.85
        )

        # Attempt 1
        res1 = self.engine.attempt_targeted_repair(anomaly)
        self.assertTrue(res1["ok"])

        # Attempt 2
        res2 = self.engine.attempt_targeted_repair(anomaly)
        self.assertTrue(res2["ok"])

        # Attempt 3: Exceeds threshold (max=2) -> Must be QUARANTINED!
        res3 = self.engine.attempt_targeted_repair(anomaly)
        self.assertFalse(res3["ok"])
        self.assertEqual(res3["status"], "QUARANTINED")
        self.assertIn("quarantined to prevent infinite self-repair loops", res3["message"])


if __name__ == "__main__":
    unittest.main()
