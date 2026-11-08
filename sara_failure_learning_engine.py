# -*- coding: utf-8 -*-
"""
SARA AI 3.0 — Self-Improvement Through Failure Analysis Engine
Captures task failures, diagnoses structural vs transient root causes, tracks failure
frequency, and formulates formal upgrade proposals without unauthorized self-modification.
"""

import os
import re
import json
import logging
import datetime
import traceback
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger("SARA.FailureLearningEngine")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [SARA.FailureLearningEngine] %(message)s")

WORKSPACE_ROOT = Path(r"D:\MARAA AI").resolve()
DATA_DIR = WORKSPACE_ROOT / "data" / "self_improvement"
DATA_DIR.mkdir(parents=True, exist_ok=True)
FAILURE_STORE_FILE = DATA_DIR / "failure_learning_store.json"


class FailureLearningEngine:
    """Diagnoses runtime task failures, builds empirical incident graphs, and initiates proposals."""

    def __init__(self):
        self.store = self._load_store()

    def _load_store(self) -> Dict[str, Any]:
        if FAILURE_STORE_FILE.exists():
            try:
                return json.loads(FAILURE_STORE_FILE.read_text(encoding="utf-8"))
            except Exception as e:
                logger.warning(f"Error reading failure learning store: {e}")
        return {"incidents": [], "patterns": {}}

    def _save_store(self):
        try:
            FAILURE_STORE_FILE.write_text(json.dumps(self.store, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            logger.error(f"Error saving failure learning store: {e}")

    def capture_failure(
        self,
        task_name: str,
        error: Any,
        stack_trace: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Diagnoses error, classifies structural vs temporary, updates pattern registry,
        and generates an upgrade proposal if structural changes are warranted.
        """
        err_str = str(error)
        st = stack_trace or traceback.format_exc()

        # 1. Classify Root Cause & Error Type
        err_type = "RuntimeError"
        for t in ["ModuleNotFoundError", "ImportError", "SyntaxError", "KeyError", "AttributeError", "TimeoutError", "ConnectionError", "PermissionError", "FileNotFoundError"]:
            if t in err_str or t in st:
                err_type = t
                break

        # 2. Determine Structural vs Temporary
        transient_types = ["TimeoutError", "ConnectionError", "RemoteDisconnected", "RateLimitError", "BusyResource"]
        is_temporary = any(tt in err_type or tt in err_str for tt in transient_types)
        classification = "TEMPORARY" if is_temporary else "STRUCTURAL"

        # 3. Component Extraction
        component = task_name
        if "ModuleNotFoundError" in err_type or "ImportError" in err_type:
            mod_match = re.search(r"No module named ['\"]([^'\"]+)['\"]", err_str)
            if mod_match:
                component = f"Dependency:{mod_match.group(1)}"
        elif "SyntaxError" in err_type:
            component = "CodebaseSyntax"

        # 4. Pattern Key & Occurrence Tracking
        pattern_key = f"{component}:{err_type}"
        patterns = self.store.setdefault("patterns", {})
        curr_pattern = patterns.get(pattern_key, {
            "count": 0,
            "first_seen": datetime.datetime.now().isoformat(),
            "component": component,
            "error_type": err_type
        })
        curr_pattern["count"] += 1
        curr_pattern["last_seen"] = datetime.datetime.now().isoformat()
        patterns[pattern_key] = curr_pattern

        incident_id = f"inc_{abs(hash(pattern_key + str(curr_pattern['count']))) % 1000000}"
        incident_record = {
            "incident_id": incident_id,
            "task_name": task_name,
            "component": component,
            "error_type": err_type,
            "classification": classification,
            "error_message": err_str,
            "stack_trace": st[:500],
            "occurrence_count": curr_pattern["count"],
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "OPEN",
            "proposal_id": None
        }

        # 5. Formulate Upgrade Proposal if Structural and Recurring (or High Impact)
        proposal_generated = False
        proposal_details = None

        if classification == "STRUCTURAL":
            from sara_capability_analyzer import capability_analyzer
            from sara_upgrade_decision_engine import upgrade_decision_engine
            from sara_upgrade_researcher import upgrade_researcher
            from sara_consent_manager import consent_manager

            diag = capability_analyzer.analyze_capability(f"Fix {component} due to {err_type}")
            decision = upgrade_decision_engine.decide_upgrade_path(diag, f"Fix {component}")
            research = upgrade_researcher.research_solution(f"Fix {component}", decision)

            proposal = consent_manager.create_proposal(
                user_request=f"Self-Improvement: Automatically address recurring failure in '{component}' ({err_type})",
                diagnosis=diag,
                decision=decision,
                research=research,
                planned_changes=[
                    f"Diagnose failure context in {component}",
                    f"Implement corrective handler or dependency patch",
                    f"Verify fix passes AST analysis and task regression test"
                ]
            )
            incident_record["proposal_id"] = proposal["proposal_id"]
            proposal_generated = True
            proposal_details = proposal

        self.store["incidents"].append(incident_record)
        self._save_store()

        return {
            "incident_id": incident_id,
            "classification": classification,
            "component": component,
            "error_type": err_type,
            "occurrence_count": curr_pattern["count"],
            "proposal_generated": proposal_generated,
            "proposal_details": proposal_details
        }

    def get_recurring_failures(self, min_occurrences: int = 2) -> List[Dict[str, Any]]:
        """Returns recurring incident patterns exceeding frequency threshold."""
        return [
            info for pat_key, info in self.store.get("patterns", {}).items()
            if info.get("count", 0) >= min_occurrences
        ]

    def resolve_incident(self, incident_id: str, resolution_notes: str) -> bool:
        """Marks an incident as formally resolved."""
        for inc in self.store.get("incidents", []):
            if inc.get("incident_id") == incident_id:
                inc["status"] = "RESOLVED"
                inc["resolution_notes"] = resolution_notes
                inc["resolved_at"] = datetime.datetime.now().isoformat()
                self._save_store()
                return True
        return False


# Global Singleton Instance
failure_learning_engine = FailureLearningEngine()

