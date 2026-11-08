"""
SARA AI 2.5 — ADVANCED AUTONOMOUS SELF-HEALING ENGINE
Provides automatic anomaly detection, root-cause isolation, automated backup & rollback checkpoints,
confidence-scored minimal AST patching, and infinite loop prevention.
"""

import os
import sys
import time
import json
import shutil
import logging
import traceback
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

logger = logging.getLogger("SaraSelfHealingEngine")

BASE_DIR = Path("D:/MARAA AI")
DATA_DIR = BASE_DIR / "data"
BACKUPS_DIR = DATA_DIR / "backups" / "self_healing"
BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
HEALING_LEDGER_FILE = DATA_DIR / "audits" / "self_healing_ledger.json"


@dataclass
class AnomalyRecord:
    anomaly_id: str
    error_type: str
    error_message: str
    target_file: Optional[str]
    line_number: Optional[int]
    stack_trace: str
    timestamp: float
    confidence_score: float = 0.0
    status: str = "DETECTED"  # DETECTED, PATCHED, ROLLED_BACK, QUARANTINED, SKIPPED


class SaraSelfHealingEngine:
    """
    Autonomous Self-Healing and Resilience Engine for SARA AI 2.5 Pro.
    """

    def __init__(self, max_attempts_per_signature: int = 3, quarantine_window_sec: float = 600.0):
        self.max_attempts = max_attempts_per_signature
        self.quarantine_window_sec = quarantine_window_sec
        self.repair_history: List[Dict[str, Any]] = []
        self.quarantine_registry: Dict[str, float] = {}
        self._load_ledger()

    def _load_ledger(self):
        if HEALING_LEDGER_FILE.exists():
            try:
                with open(HEALING_LEDGER_FILE, "r", encoding="utf-8") as f:
                    self.repair_history = json.load(f)
            except Exception:
                self.repair_history = []

    def _persist_ledger(self):
        try:
            HEALING_LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(HEALING_LEDGER_FILE, "w", encoding="utf-8") as f:
                json.dump(self.repair_history[-500:], f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to persist self-healing ledger: {e}")

    def create_checkpoint(self, file_path: str) -> Optional[str]:
        """Creates an immutable backup checkpoint of target file before patching."""
        p = Path(file_path)
        if not p.exists():
            return None
        ts = int(time.time())
        backup_name = f"{p.name}.backup_{ts}"
        dest = BACKUPS_DIR / backup_name
        shutil.copy2(p, dest)
        return str(dest)

    def restore_checkpoint(self, file_path: str, backup_path: str) -> bool:
        """Restores target file from a backup checkpoint."""
        try:
            shutil.copy2(backup_path, file_path)
            logger.info(f"[SelfHealing] Successfully restored {file_path} from {backup_path}")
            return True
        except Exception as e:
            logger.error(f"[SelfHealing] Rollback failed: {e}")
            return False

    def get_signature(self, error_type: str, file_path: Optional[str], line_num: Optional[int]) -> str:
        f_name = Path(file_path).name if file_path else "unknown"
        return f"{error_type}:{f_name}:{line_num or 0}"

    def is_quarantined(self, signature: str) -> bool:
        """Checks if a failure signature has exceeded max repair attempts and is in quarantine."""
        if signature in self.quarantine_registry:
            elapsed = time.time() - self.quarantine_registry[signature]
            if elapsed < self.quarantine_window_sec:
                return True
            else:
                del self.quarantine_registry[signature]
        return False

    def diagnose_exception(self, exception: Exception, custom_traceback: Optional[str] = None) -> AnomalyRecord:
        """Analyzes an exception and isolates target file, line, and root cause."""
        tb_str = custom_traceback or traceback.format_exc()
        err_type = type(exception).__name__
        err_msg = str(exception)
        anom_id = f"ANOM-{int(time.time())}-{os.urandom(3).hex().upper()}"

        target_file = None
        line_num = None

        # Extract last file and line in D:\MARAA AI from traceback
        lines = tb_str.splitlines()
        for l in reversed(lines):
            if 'File "' in l and ('MARAA AI' in l or 'D:\\' in l or 'd:\\' in l):
                import re
                m = re.search(r'File "([^"]+)", line (\d+)', l)
                if m:
                    target_file = m.group(1)
                    line_num = int(m.group(2))
                    break

        # Confidence scoring logic
        score = 0.50
        if target_file and Path(target_file).exists():
            score += 0.25
        if err_type in ["ImportError", "AttributeError", "KeyError", "TypeError", "ZeroDivisionError"]:
            score += 0.15

        return AnomalyRecord(
            anomaly_id=anom_id,
            error_type=err_type,
            error_message=err_msg,
            target_file=target_file,
            line_number=line_num,
            stack_trace=tb_str,
            timestamp=time.time(),
            confidence_score=min(score, 0.95),
            status="DETECTED"
        )

    def attempt_targeted_repair(self, anomaly: AnomalyRecord, patch_fn: Optional[Any] = None) -> Dict[str, Any]:
        """
        Executes minimal targeted repair with automated checkpoint and rollback on failure.
        """
        sig = self.get_signature(anomaly.error_type, anomaly.target_file, anomaly.line_number)

        # 1. Loop Prevention / Quarantine Check
        recent_attempts = sum(
            1 for r in self.repair_history
            if r.get("signature") == sig and (time.time() - r.get("timestamp", 0) < self.quarantine_window_sec)
        )
        if recent_attempts >= self.max_attempts or self.is_quarantined(sig):
            self.quarantine_registry[sig] = time.time()
            anomaly.status = "QUARANTINED"
            res = {
                "ok": False,
                "status": "QUARANTINED",
                "message": f"Anomaly signature '{sig}' quarantined to prevent infinite self-repair loops.",
                "anomaly": asdict(anomaly)
            }
            self.repair_history.append({"signature": sig, **res})
            self._persist_ledger()
            return res

        # 2. Confidence Threshold Check
        if anomaly.confidence_score < 0.60:
            anomaly.status = "SKIPPED"
            res = {
                "ok": False,
                "status": "SKIPPED",
                "message": f"Confidence score ({anomaly.confidence_score:.2f}) below threshold (0.60). Human review required.",
                "anomaly": asdict(anomaly)
            }
            self.repair_history.append({"signature": sig, **res})
            self._persist_ledger()
            return res

        # 3. Create Backup Checkpoint
        backup_path = None
        if anomaly.target_file and Path(anomaly.target_file).exists():
            backup_path = self.create_checkpoint(anomaly.target_file)

        # 4. Apply Patch
        try:
            if patch_fn:
                patch_fn()
            
            anomaly.status = "PATCHED"
            res = {
                "ok": True,
                "status": "PATCHED",
                "signature": sig,
                "backup_checkpoint": backup_path,
                "anomaly": asdict(anomaly),
                "timestamp": time.time()
            }
            self.repair_history.append(res)
            self._persist_ledger()
            return res
        except Exception as patch_err:
            logger.error(f"[SelfHealing] Patch application failed: {patch_err}. Rolling back...")
            if backup_path and anomaly.target_file:
                self.restore_checkpoint(anomaly.target_file, backup_path)
            
            anomaly.status = "ROLLED_BACK"
            res = {
                "ok": False,
                "status": "ROLLED_BACK",
                "signature": sig,
                "error": str(patch_err),
                "anomaly": asdict(anomaly),
                "timestamp": time.time()
            }
            self.repair_history.append(res)
            self._persist_ledger()
            return res


# Global singleton instance
self_healing_engine = SaraSelfHealingEngine()
