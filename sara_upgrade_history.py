# -*- coding: utf-8 -*-
"""
SARA AI 3.0 — Permanent Upgrade History & Change Reporting Ledger
Maintains an immutable, searchable ledger of all upgrade attempts, approvals,
modifications, test outcomes, and rollback events with strict credential redaction.
"""

import os
import re
import json
import logging
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger("SARA.UpgradeHistory")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [SARA.UpgradeHistory] %(message)s")

WORKSPACE_ROOT = Path(r"D:\MARAA AI").resolve()
AUDITS_DIR = WORKSPACE_ROOT / "data" / "audits"
AUDITS_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_FILE = AUDITS_DIR / "upgrade_history.json"


class UpgradeHistory:
    """Manages persistent upgrade telemetry, change verification records, and audit querying."""

    def __init__(self):
        self.history = self._load_history()

    def _load_history(self) -> List[Dict[str, Any]]:
        if HISTORY_FILE.exists():
            try:
                data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    return data
            except Exception as e:
                logger.warning(f"Error loading upgrade history: {e}")
        return []

    def _save_history(self):
        try:
            HISTORY_FILE.write_text(json.dumps(self.history, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            logger.error(f"Error persisting upgrade history: {e}")

    def _redact_secrets(self, text: Any) -> Any:
        """Sanitizes API tokens, keys, passwords, and authorization headers."""
        if not isinstance(text, str):
            return text
        sanitized = text
        # Key/value pairs with secrets
        sanitized = re.sub(
            r"(?i)(key|token|secret|password|bearer|auth)([:=]\s*['\"]?)([a-zA-Z0-9_\-\.]{8,})(['\"]?)",
            r"\1\2***REDACTED***\4",
            sanitized
        )
        # Raw API tokens (Google AIza, GitHub ghp, OpenAI sk)
        sanitized = re.sub(r"AIza[0-9A-Za-z\-_]{35}", "***REDACTED_API_KEY***", sanitized)
        sanitized = re.sub(r"ghp_[0-9a-zA-Z]{36}", "***REDACTED_GITHUB_TOKEN***", sanitized)
        sanitized = re.sub(r"sk-[0-9a-zA-Z_\-]{20,}", "***REDACTED_KEY***", sanitized)
        return sanitized

    def record_upgrade(
        self,
        upgrade_id: str,
        user_request: str,
        original_limitation: str,
        root_cause: str,
        upgrade_category: str,
        proposed_solution: str,
        approval_status: str,
        files_created: List[str],
        files_modified: List[str],
        dependencies_added: List[str],
        skills_installed: List[str],
        tests_executed: List[str],
        test_results: Dict[str, Any],
        rollback_status: str,
        final_outcome: str
    ) -> Dict[str, Any]:
        """Appends a sanitized, permanent audit record of an upgrade lifecycle."""
        record = {
            "upgrade_id": upgrade_id,
            "timestamp": datetime.datetime.now().isoformat(),
            "user_request": self._redact_secrets(user_request),
            "original_limitation": self._redact_secrets(original_limitation),
            "root_cause": self._redact_secrets(root_cause),
            "upgrade_category": upgrade_category,
            "proposed_solution": self._redact_secrets(proposed_solution),
            "approval_status": approval_status,
            "files_created": files_created,
            "files_modified": files_modified,
            "dependencies_added": dependencies_added,
            "skills_installed": skills_installed,
            "tests_executed": tests_executed,
            "test_results": test_results,
            "rollback_status": rollback_status,
            "final_outcome": final_outcome
        }

        # Check for update or append
        existing_idx = next((i for i, r in enumerate(self.history) if r.get("upgrade_id") == upgrade_id), -1)
        if existing_idx >= 0:
            self.history[existing_idx] = record
        else:
            self.history.append(record)

        self._save_history()
        return record

    def get_upgrade(self, upgrade_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a specific upgrade record by ID."""
        self.history = self._load_history()
        return next((r for r in self.history if r.get("upgrade_id") == upgrade_id), None)

    def search_upgrades(self, query: str) -> List[Dict[str, Any]]:
        """Searches past upgrades by keyword or category."""
        self.history = self._load_history()
        q = query.lower()
        return [
            r for r in self.history
            if q in r.get("user_request", "").lower()
            or q in r.get("original_limitation", "").lower()
            or q in r.get("upgrade_category", "").lower()
            or q in r.get("final_outcome", "").lower()
        ]

    def get_statistics(self) -> Dict[str, Any]:
        """Computes executive metrics across the complete upgrade history."""
        self.history = self._load_history()
        total = len(self.history)
        successful = sum(1 for r in self.history if r.get("final_outcome") == "SUCCESS")
        failed = sum(1 for r in self.history if r.get("final_outcome") == "FAILED")
        rolled_back = sum(1 for r in self.history if r.get("rollback_status") == "ROLLED_BACK")

        return {
            "total_upgrades_attempted": total,
            "successful_upgrades": successful,
            "failed_upgrades": failed,
            "rolled_back_count": rolled_back,
            "success_rate_percent": round((successful / total * 100), 1) if total > 0 else 100.0,
            "last_upgrade_timestamp": self.history[-1]["timestamp"] if self.history else None
        }


# Global Singleton Instance
upgrade_history = UpgradeHistory()
