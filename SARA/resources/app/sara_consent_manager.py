# -*- coding: utf-8 -*-
"""
SARA AI 3.0 — User Consent & Explicit Approval Gate
Enforces strict human-in-the-loop authorization boundaries. Never modifies code,
installs dependencies, or alters system architecture without explicit, proposal-bound consent.
"""

import os
import json
import time
import hashlib
import logging
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger("SARA.ConsentManager")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [SARA.ConsentManager] %(message)s")

WORKSPACE_ROOT = Path(r"D:\MARAA AI").resolve()
DATA_DIR = WORKSPACE_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
SELF_IMPROVE_DIR = DATA_DIR / "self_improvement"
SELF_IMPROVE_DIR.mkdir(parents=True, exist_ok=True)

PROPOSALS_DB = SELF_IMPROVE_DIR / "proposals.json"


class ConsentManager:
    """Manages the formal proposal, approval, rejection, and modification lifecycle."""

    def __init__(self):
        self.proposals = self._load_proposals()

    def _load_proposals(self) -> Dict[str, Any]:
        data = {"pending": {}, "approved": {}, "rejected": {}, "completed": {}}
        if PROPOSALS_DB.exists():
            try:
                loaded = json.loads(PROPOSALS_DB.read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    data.update(loaded)
            except Exception as e:
                logger.warning(f"Error reading proposals database: {e}")
        # Ensure mandatory keys exist
        for k in ["pending", "approved", "rejected", "completed"]:
            if k not in data:
                data[k] = {}
        return data

    def _save_proposals(self):
        try:
            PROPOSALS_DB.write_text(json.dumps(self.proposals, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            logger.error(f"Error persisting proposals: {e}")

    def _compute_fingerprint(self, feature_name: str, target_files: List[str], planned_changes: List[str]) -> str:
        payload = f"{feature_name}|{','.join(sorted(target_files))}|{';'.join(planned_changes)}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

    def create_proposal(
        self,
        user_request: str,
        diagnosis: Dict[str, Any],
        decision: Dict[str, Any],
        research: Dict[str, Any],
        planned_changes: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Creates a structured, cryptographically identified upgrade proposal.
        """
        feature_name = decision.get("target_component") or research.get("recommended_approach", {}).get("name", "New Capability")
        target_files = research.get("target_files", [])
        category = decision.get("decision_category", "NEW_FEATURE")
        risk_level = decision.get("risk_level", "MEDIUM")
        complexity = research.get("estimated_complexity", "Medium")

        if not planned_changes:
            planned_changes = [
                f"Implement core logic in {target_files[0] if target_files else 'dedicated module'}",
                "Integrate with SARA neural brain / fast-path dispatcher",
                "Update tool registry and verify zero regressions",
                "Execute automated capability acceptance test"
            ]

        fingerprint = self._compute_fingerprint(feature_name, target_files, planned_changes)
        proposal_id = f"prop_{fingerprint[:10]}"

        # Format Human-Facing Markdown Proposal
        proposal_text = (
            f"I investigated the existing system regarding: \"{user_request}\"\n\n"
            f"PROPOSED ACTION:\n\n"
            f"Type: {category.replace('_', ' ').title()}\n"
            f"Feature: {feature_name}\n\n"
            f"Planned changes:\n"
            + "\n".join(f"{idx+1}. {step}" for idx, step in enumerate(planned_changes))
            + "\n\n"
            f"Files expected to change:\n"
            + "\n".join(f"- {f}" for f in target_files)
            + "\n\n"
            f"Dependencies:\n"
            f"- Verified local assets and existing dependencies ({', '.join(research.get('dependencies_required', [])) or 'None additional'}).\n\n"
            f"Risks:\n"
            f"- {risk_level} risk level. Full rollback checkpoint will be captured before applying any change.\n\n"
            f"Estimated complexity: {complexity}.\n\n"
            f"Would you like me to implement this upgrade?"
        )

        record = {
            "proposal_id": proposal_id,
            "fingerprint": fingerprint,
            "created_at": datetime.datetime.now().isoformat(),
            "user_request": user_request,
            "category": category,
            "feature_name": feature_name,
            "planned_changes": planned_changes,
            "target_files": target_files,
            "risk_level": risk_level,
            "complexity": complexity,
            "status": "PENDING_APPROVAL",
            "formatted_proposal": proposal_text,
            "approval_metadata": None
        }

        self.proposals["pending"][proposal_id] = record
        self._save_proposals()

        return record

    def approve_proposal(self, proposal_id: str, approver: str = "Pasha Dev") -> Dict[str, Any]:
        """Explicitly grants approval for a specific proposal ID and exact fingerprint."""
        if proposal_id not in self.proposals["pending"]:
            return {
                "success": False,
                "error": f"Proposal ID '{proposal_id}' not found in pending state."
            }

        prop = self.proposals["pending"].pop(proposal_id)
        prop["status"] = "APPROVED"
        prop["approval_metadata"] = {
            "approved_by": approver,
            "approved_at": datetime.datetime.now().isoformat(),
            "authorized_fingerprint": prop["fingerprint"]
        }

        self.proposals["approved"][proposal_id] = prop
        self._save_proposals()

        return {
            "success": True,
            "proposal_id": proposal_id,
            "status": "APPROVED",
            "fingerprint": prop["fingerprint"],
            "message": f"Upgrade proposal '{proposal_id}' has been explicitly authorized."
        }

    def reject_proposal(self, proposal_id: str, reason: str = "User declined") -> Dict[str, Any]:
        """Rejects a pending proposal and guarantees no files are modified."""
        if proposal_id not in self.proposals["pending"]:
            return {
                "success": False,
                "error": f"Proposal ID '{proposal_id}' not found in pending state."
            }

        prop = self.proposals["pending"].pop(proposal_id)
        prop["status"] = "REJECTED"
        prop["rejection_metadata"] = {
            "rejected_at": datetime.datetime.now().isoformat(),
            "reason": reason
        }

        self.proposals["rejected"][proposal_id] = prop
        self._save_proposals()

        return {
            "success": True,
            "proposal_id": proposal_id,
            "status": "REJECTED",
            "message": f"Upgrade proposal '{proposal_id}' was rejected. Zero modifications performed."
        }

    def modify_proposal(self, proposal_id: str, modifications: Dict[str, Any]) -> Dict[str, Any]:
        """Updates proposal specifications and re-sets status to PENDING_APPROVAL with new fingerprint."""
        prop = self.proposals["pending"].get(proposal_id) or self.proposals["approved"].get(proposal_id)
        if not prop:
            return {"success": False, "error": f"Proposal '{proposal_id}' not found."}

        # Apply allowed modifications
        if "planned_changes" in modifications:
            prop["planned_changes"] = modifications["planned_changes"]
        if "target_files" in modifications:
            prop["target_files"] = modifications["target_files"]
        if "risk_level" in modifications:
            prop["risk_level"] = modifications["risk_level"]

        # Recompute fingerprint
        new_fingerprint = self._compute_fingerprint(prop["feature_name"], prop["target_files"], prop["planned_changes"])
        prop["fingerprint"] = new_fingerprint
        prop["status"] = "PENDING_APPROVAL"
        prop["approval_metadata"] = None
        prop["modified_at"] = datetime.datetime.now().isoformat()

        # Ensure in pending
        self.proposals["pending"][proposal_id] = prop
        if proposal_id in self.proposals["approved"]:
            del self.proposals["approved"][proposal_id]

        self._save_proposals()

        return {
            "success": True,
            "proposal_id": proposal_id,
            "status": "PENDING_APPROVAL",
            "new_fingerprint": new_fingerprint,
            "message": "Proposal modified. Explicit approval required for updated specifications."
        }

    def explain_more(self, proposal_id: str) -> Dict[str, Any]:
        """Generates in-depth architectural and safety rationale for the user."""
        prop = (
            self.proposals["pending"].get(proposal_id)
            or self.proposals["approved"].get(proposal_id)
            or self.proposals["rejected"].get(proposal_id)
        )
        if not prop:
            return {"success": False, "error": f"Proposal '{proposal_id}' not found."}

        explanation = (
            f"ARCHITECTURAL EXPLANATION FOR PROPOSAL: {proposal_id}\n\n"
            f"1. Why this solution: It fulfills '{prop['user_request']}' with the smallest viable diff.\n"
            f"2. Safety Guarantee: A pre-upgrade snapshot is saved to 'data/backups/upgrades/{proposal_id}/'.\n"
            f"3. Regression Verification: Automated test suite will be executed before finalizing.\n"
            f"4. Isolation: Only target files {prop['target_files']} are accessed.\n"
            f"5. Rollback: If tests fail or syntax errors occur, files are restored within 500ms."
        )
        return {
            "success": True,
            "proposal_id": proposal_id,
            "explanation": explanation
        }

    def validate_authorization(self, proposal_id: str, expected_fingerprint: str) -> bool:
        """
        Guarantees that an execution is strictly authorized for this exact proposal ID and fingerprint.
        A generic previous approval can NEVER authorize unrelated modifications.
        """
        if proposal_id not in self.proposals["approved"]:
            logger.error(f"Unauthorized execution attempt: Proposal '{proposal_id}' is not in approved state.")
            return False

        prop = self.proposals["approved"][proposal_id]
        if prop.get("fingerprint") != expected_fingerprint:
            logger.error(f"Fingerprint mismatch: Proposal '{proposal_id}' fingerprint differs from execution payload.")
            return False

        return True


# Global Singleton Instance
consent_manager = ConsentManager()
