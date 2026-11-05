# -*- coding: utf-8 -*-
"""
SARA AI 2.5 Pro — Controlled Self-Improvement & Capability Assessment Engine
Evaluates capability health, detects deficiencies, formulates structured upgrade
proposals, guards against infinite improvement loops, and submits tasks to Antigravity.
"""

import os
import sys
import json
import time
import hashlib
import datetime
from pathlib import Path

WORKSPACE_ROOT = Path(r"D:\MARAA AI").resolve()
SELF_IMPROVE_DIR = WORKSPACE_ROOT / "data" / "self_improvement"
SELF_IMPROVE_DIR.mkdir(parents=True, exist_ok=True)

ASSESSMENT_FILE = SELF_IMPROVE_DIR / "weekly_assessment.json"
PROPOSALS_FILE = SELF_IMPROVE_DIR / "proposals.json"

MAX_RETRIES_PER_MODULE = 3


class SelfImprovementEngine:

    def __init__(self):
        self.proposals = self.load_proposals()

    def load_proposals(self) -> dict:
        if PROPOSALS_FILE.exists():
            try:
                return json.loads(PROPOSALS_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"active": {}, "completed": {}, "rejected": {}}

    def save_proposals(self):
        try:
            PROPOSALS_FILE.write_text(
                json.dumps(self.proposals, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
        except Exception as e:
            print(f"[SelfImprovement] Save proposals failed: {e}")

    def evaluate_system_capabilities(self) -> dict:
        """Evaluates tools, logs, and known subsystems for health and deficits."""
        t0 = time.perf_counter()
        findings = []

        # 1. Check Antigravity Bridge
        agy_cli = Path(r"C:\Users\USER\AppData\Local\agy\bin\agy.exe")
        if not agy_cli.exists():
            findings.append({
                "component": "Antigravity Bridge",
                "severity": "HIGH",
                "observation": "agy.exe executable missing from standard AppData path."
            })

        # 2. Check 3D Character Textures & Model
        model_pmx = WORKSPACE_ROOT / "SARA/resources/app/assets/characters/evelyn/model.pmx"
        if not model_pmx.exists():
            findings.append({
                "component": "3D Character Asset",
                "severity": "CRITICAL",
                "observation": "Signature Evelyn PMX model is missing."
            })

        # 3. Check Memory Stores
        mem_file = WORKSPACE_ROOT / "SARA/resources/app/memories.json"
        if not mem_file.exists():
            findings.append({
                "component": "Semantic Memory",
                "severity": "MEDIUM",
                "observation": "memories.json not found."
            })

        assessment = {
            "assessment_id": f"eval_{int(time.time())}",
            "generated_at": datetime.datetime.now().isoformat(),
            "overall_health": "OPTIMAL" if not findings else ("DEGRADED" if any(f["severity"] == "HIGH" for f in findings) else "ATTENTION_NEEDED"),
            "total_deficiencies_found": len(findings),
            "findings": findings,
            "metrics": {
                "evaluation_duration_ms": round((time.perf_counter() - t0) * 1000, 2),
                "active_proposals_count": len(self.proposals.get("active", {})),
                "completed_upgrades_count": len(self.proposals.get("completed", {}))
            }
        }

        # Persist weekly assessment
        ASSESSMENT_FILE.write_text(json.dumps(assessment, indent=2, ensure_ascii=False), encoding="utf-8")
        return assessment

    def create_upgrade_proposal(
        self,
        component: str,
        observed_problem: str,
        proposed_solution: str,
        target_files: list,
        confidence: float = 0.95,
        risk_level: str = "LOW",
        acceptance_criteria: list = None
    ) -> dict:
        """
        Constructs a structured upgrade proposal, checking for duplicate tasks
        and enforcing loop prevention guardrails.
        """
        # Generate signature hash to prevent duplicate submissions
        sig_str = f"{component}:{observed_problem.strip().lower()}"
        sig_hash = hashlib.sha256(sig_str.encode()).hexdigest()[:10]

        # Check loop prevention
        if sig_hash in self.proposals["active"]:
            existing = self.proposals["active"][sig_hash]
            retry_count = existing.get("retry_count", 1)
            if retry_count >= MAX_RETRIES_PER_MODULE:
                return {
                    "success": False,
                    "rejected": True,
                    "reason": f"Loop prevention triggered: '{component}' exceeded max retries ({MAX_RETRIES_PER_MODULE}).",
                    "proposal_id": sig_hash
                }
            existing["retry_count"] = retry_count + 1
            self.save_proposals()
            return {
                "success": True,
                "status": "RETRY_QUEUED",
                "proposal": existing
            }

        proposal = {
            "proposal_id": sig_hash,
            "component": component,
            "observed_problem": observed_problem,
            "proposed_solution": proposed_solution,
            "target_files": target_files,
            "confidence": confidence,
            "risk_level": risk_level,
            "acceptance_criteria": acceptance_criteria or ["Automated tests pass with zero regressions."],
            "status": "PENDING_AUTHORIZATION",
            "retry_count": 1,
            "created_at": datetime.datetime.now().isoformat()
        }

        self.proposals["active"][sig_hash] = proposal
        self.save_proposals()

        return {
            "success": True,
            "status": "PROPOSED",
            "proposal": proposal
        }

    def dispatch_proposal_to_antigravity(self, proposal_id: str) -> dict:
        """Converts an active proposal into an Antigravity development task."""
        if proposal_id not in self.proposals["active"]:
            return {"success": False, "error": f"Proposal {proposal_id} not found in active proposals."}

        prop = self.proposals["active"][proposal_id]
        from sara_antigravity_bridge import bridge

        task = bridge.prepare_development_task(
            objective=f"Self-Improvement: {prop['component']}",
            problem_statement=prop["observed_problem"],
            expected_behavior=prop["proposed_solution"],
            relevant_files=prop["target_files"],
            acceptance_criteria=prop["acceptance_criteria"],
            risk_level=prop["risk_level"]
        )

        sub_res = bridge.submit_development_task(task)
        prop["antigravity_task_id"] = task["task_id"]
        prop["status"] = "DISPATCHED_TO_ANTIGRAVITY"
        self.save_proposals()

        return {
            "success": True,
            "proposal_id": proposal_id,
            "antigravity_task_id": task["task_id"],
            "message": f"Proposal dispatched to Antigravity IDE: {task['task_id']}"
        }


self_improvement = SelfImprovementEngine()
SaraSelfImprovement = SelfImprovementEngine
sara_self_improvement = self_improvement
SelfImprovementEngine.get_improvement_status = lambda self: "active"

if __name__ == "__main__":
    report = self_improvement.evaluate_system_capabilities()
    print("Self-Improvement Assessment Report:")
    print(json.dumps(report, indent=2))
