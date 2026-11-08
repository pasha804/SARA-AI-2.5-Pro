# -*- coding: utf-8 -*-
"""
SARA AI 3.0 — Autonomous Capability Detection & Analysis Engine
Inspects registered tools, skills, automations, and subsystem handlers to
determine whether a user request is supported, broken, partial, or missing.
"""

import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger("SARA.CapabilityAnalyzer")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [SARA.CapabilityAnalyzer] %(message)s")

WORKSPACE_ROOT = Path(r"D:\MARAA AI").resolve()
DATA_DIR = WORKSPACE_ROOT / "data"
AUDITS_DIR = DATA_DIR / "audits"
SKILLS_DIR = WORKSPACE_ROOT / ".agents" / "skills"
GLOBAL_SKILLS_DIR = Path(r"C:\Users\USER\.gemini\config\skills")

# Capability Status Taxonomy
STATUS_EXISTS_FUNCTIONAL = "EXISTS_FUNCTIONAL"
STATUS_EXISTS_BROKEN = "EXISTS_BROKEN"
STATUS_EXISTS_PARTIAL = "EXISTS_PARTIAL"
STATUS_EXISTS_UNCONFIGURED = "EXISTS_UNCONFIGURED"
STATUS_PERMISSION_MISSING = "PERMISSION_MISSING"
STATUS_COMPLETELY_MISSING = "COMPLETELY_MISSING"
STATUS_NOT_SUPPORTED_SAFETY = "NOT_SUPPORTED_SAFETY"


class CapabilityAnalyzer:
    """Forensic inspector of SARA's runtime capabilities and limitations."""

    def __init__(self):
        self.tools = self._load_tool_registry()
        self.automations = self._load_automation_registry()
        self.skills = self._discover_installed_skills()

    def _load_tool_registry(self) -> List[Dict[str, Any]]:
        tool_file = AUDITS_DIR / "tool_registry.json"
        if tool_file.exists():
            try:
                data = json.loads(tool_file.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    return data
                if isinstance(data, dict) and "tools" in data:
                    return data["tools"]
            except Exception as e:
                logger.warning(f"Failed to load tool registry: {e}")
        return []

    def _load_automation_registry(self) -> List[Dict[str, Any]]:
        auto_file = AUDITS_DIR / "automation_registry.json"
        if auto_file.exists():
            try:
                data = json.loads(auto_file.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    return data
                if isinstance(data, dict) and "automations" in data:
                    return data["automations"]
            except Exception as e:
                logger.warning(f"Failed to load automation registry: {e}")
        return []

    def _discover_installed_skills(self) -> List[Dict[str, Any]]:
        found = []
        # Local workspace skills
        if SKILLS_DIR.exists():
            for sdir in SKILLS_DIR.iterdir():
                if sdir.is_dir() and (sdir / "SKILL.md").exists():
                    found.append({
                        "name": sdir.name,
                        "location": str(sdir / "SKILL.md"),
                        "scope": "workspace"
                    })
        # Global installed skills
        if GLOBAL_SKILLS_DIR.exists():
            for sdir in GLOBAL_SKILLS_DIR.iterdir():
                if sdir.is_dir() and (sdir / "SKILL.md").exists():
                    found.append({
                        "name": sdir.name,
                        "location": str(sdir / "SKILL.md"),
                        "scope": "global"
                    })
        return found

    def refresh(self):
        """Reload registries and skills to reflect runtime state."""
        self.tools = self._load_tool_registry()
        self.automations = self._load_automation_registry()
        self.skills = self._discover_installed_skills()

    def analyze_capability(self, user_intent: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Exhaustively analyzes whether SARA can fulfill the requested capability.
        Returns a structured diagnostic assessment.
        """
        self.refresh()
        intent = (user_intent or "").strip()
        intent_lower = intent.lower()

        # 1. Safety & Feasibility Filter
        safety_keywords = [
            "hack", "bypass aes", "decrypt rsa private key without key",
            "physical hardware rewrite", "overclock cpu to 10ghz",
            "ddos", "ransomware", "delete windows kernel", "malware"
        ]
        if any(sk in intent_lower for sk in safety_keywords):
            return {
                "capability_id": f"cap_{abs(hash(intent)) % 1000000}",
                "user_intent": intent,
                "status": STATUS_NOT_SUPPORTED_SAFETY,
                "confidence": 1.0,
                "diagnostic_details": "Request violates fundamental safety, encryption physics, or legal boundaries.",
                "matched_tools": [],
                "matched_skills": [],
                "matched_automations": [],
                "missing_elements": ["Request is fundamentally unsupported or unsafe"],
                "recommended_action": "REJECT_UNSUPPORTED"
            }

        # 2. Tokenize intent keywords
        tokens = set(re.findall(r"\b[a-zA-Z0-9_\-]{3,}\b", intent_lower))
        stop_words = {"can", "you", "please", "could", "would", "how", "what", "with", "this", "that", "the", "and", "for"}
        query_terms = [t for t in tokens if t not in stop_words]

        # 3. Match Tools
        matched_tools = []
        for t in self.tools:
            name = t.get("name", "").lower()
            desc = t.get("description", "").lower()
            cat = t.get("category", "").lower()
            hits = sum(1 for term in query_terms if term in name or term in desc or term in cat)
            if hits > 0:
                matched_tools.append({
                    "name": t.get("name"),
                    "category": t.get("category"),
                    "operational_status": t.get("operational_status", "UNKNOWN"),
                    "relevance_score": hits
                })
        matched_tools.sort(key=lambda x: x["relevance_score"], reverse=True)

        # 4. Match Skills
        matched_skills = []
        for s in self.skills:
            name = s.get("name", "").lower()
            hits = sum(1 for term in query_terms if term in name)
            if hits > 0:
                matched_skills.append({
                    "name": s.get("name"),
                    "location": s.get("location"),
                    "scope": s.get("scope"),
                    "relevance_score": hits
                })
        matched_skills.sort(key=lambda x: x["relevance_score"], reverse=True)

        # 5. Match Automations
        matched_automations = []
        for a in self.automations:
            name = a.get("name", "").lower()
            cat = a.get("category", "").lower()
            hits = sum(1 for term in query_terms if term in name or term in cat)
            if hits > 0:
                matched_automations.append({
                    "name": a.get("name"),
                    "category": a.get("category"),
                    "status": a.get("status"),
                    "relevance_score": hits
                })
        matched_automations.sort(key=lambda x: x["relevance_score"], reverse=True)

        # 6. Check Specific Deficit Scenarios
        # Scenario A: Broken Feature
        for mt in matched_tools:
            if mt.get("operational_status") in ["FAILING", "BROKEN"]:
                return {
                    "capability_id": f"cap_{abs(hash(intent)) % 1000000}",
                    "user_intent": intent,
                    "status": STATUS_EXISTS_BROKEN,
                    "confidence": 0.95,
                    "diagnostic_details": f"Matching tool '{mt['name']}' exists but is currently flagged as {mt['operational_status']}.",
                    "matched_tools": matched_tools[:5],
                    "matched_skills": matched_skills[:3],
                    "matched_automations": matched_automations[:3],
                    "missing_elements": [f"Execution handler for {mt['name']} is failing"],
                    "recommended_action": "PROPOSE_FEATURE_FIX"
                }

        # Scenario B: Existing Functional (Exact or High Match)
        if matched_tools and matched_tools[0]["relevance_score"] >= max(2, len(query_terms)):
            best_tool = matched_tools[0]
            if best_tool.get("operational_status") in ["VERIFIED_WORKING", "WORKING_WITH_WARNINGS"]:
                # Check if user specifically requested an improvement or extension
                if any(k in intent_lower for k in ["improve", "upgrade", "enhance", "add support for", "extend", "faster", "more features"]):
                    return {
                        "capability_id": f"cap_{abs(hash(intent)) % 1000000}",
                        "user_intent": intent,
                        "status": STATUS_EXISTS_PARTIAL,
                        "confidence": 0.90,
                        "diagnostic_details": f"Tool '{best_tool['name']}' already exists and functions, but user requested an enhancement or additional capability.",
                        "matched_tools": matched_tools[:5],
                        "matched_skills": matched_skills[:3],
                        "matched_automations": matched_automations[:3],
                        "missing_elements": ["Extended feature options requested by user"],
                        "recommended_action": "PROPOSE_FEATURE_UPGRADE"
                    }
                return {
                    "capability_id": f"cap_{abs(hash(intent)) % 1000000}",
                    "user_intent": intent,
                    "status": STATUS_EXISTS_FUNCTIONAL,
                    "confidence": 0.95,
                    "diagnostic_details": f"Capability is fully covered by existing verified tool '{best_tool['name']}'.",
                    "matched_tools": matched_tools[:5],
                    "matched_skills": matched_skills[:3],
                    "matched_automations": matched_automations[:3],
                    "missing_elements": [],
                    "recommended_action": "EXECUTE_EXISTING_TOOL"
                }

        # Scenario C: Partial Matches (e.g. GitHub analysis where basic git or repo tools exist, but specialized workflow missing)
        if matched_tools or matched_skills or matched_automations:
            return {
                "capability_id": f"cap_{abs(hash(intent)) % 1000000}",
                "user_intent": intent,
                "status": STATUS_EXISTS_PARTIAL,
                "confidence": 0.85,
                "diagnostic_details": f"Partial components exist ({len(matched_tools)} tools, {len(matched_skills)} skills), but full workflow '{intent}' is not consolidated.",
                "matched_tools": matched_tools[:5],
                "matched_skills": matched_skills[:3],
                "matched_automations": matched_automations[:3],
                "missing_elements": [f"Dedicated orchestrated workflow for '{intent}'"],
                "recommended_action": "PROPOSE_NEW_FEATURE_OR_UPGRADE"
            }

        # Scenario D: Completely Missing
        return {
            "capability_id": f"cap_{abs(hash(intent)) % 1000000}",
            "user_intent": intent,
            "status": STATUS_COMPLETELY_MISSING,
            "confidence": 0.98,
            "diagnostic_details": f"No existing tool, skill, or automation matches intent '{intent}'.",
            "matched_tools": [],
            "matched_skills": [],
            "matched_automations": [],
            "missing_elements": [f"No tool or integration found for: {intent}"],
            "recommended_action": "PROPOSE_NEW_CAPABILITY"
        }


# Global Singleton Instance
capability_analyzer = CapabilityAnalyzer()
