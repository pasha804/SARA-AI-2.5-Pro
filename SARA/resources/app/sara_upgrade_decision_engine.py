# -*- coding: utf-8 -*-
"""
SARA AI 3.0 — Upgrade vs New Feature Decision Engine
Classifies capability requests into 8 strict decision categories (A through H)
and enforces the Smallest Reliable Solution rule to prevent duplicate tools.
"""

import os
import re
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("SARA.UpgradeDecisionEngine")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [SARA.UpgradeDecisionEngine] %(message)s")

# Decision Categories
CAT_A_EXISTING_FEATURE_FIX = "EXISTING_FEATURE_FIX"
CAT_B_EXISTING_FEATURE_UPGRADE = "EXISTING_FEATURE_UPGRADE"
CAT_C_NEW_FEATURE = "NEW_FEATURE"
CAT_D_NEW_TOOL = "NEW_TOOL"
CAT_E_NEW_SKILL = "NEW_SKILL"
CAT_F_NEW_INTEGRATION = "NEW_INTEGRATION"
CAT_G_CONFIGURATION_REQUIRED = "CONFIGURATION_REQUIRED"
CAT_H_NOT_FEASIBLE = "NOT_FEASIBLE"


class UpgradeDecisionEngine:
    """Enforces optimal architectural decisions and duplicate elimination."""

    def decide_upgrade_path(self, diagnosis: Dict[str, Any], user_request: str) -> Dict[str, Any]:
        """
        Classifies diagnosis into categories A through H and recommends the smallest viable path.
        """
        status = diagnosis.get("status", "")
        intent_lower = (user_request or "").lower()
        matched_tools = diagnosis.get("matched_tools", [])
        matched_skills = diagnosis.get("matched_skills", [])

        # 1. Category H: NOT FEASIBLE / UNSAFE
        if status == "NOT_SUPPORTED_SAFETY" or any(k in intent_lower for k in [
            "break physics", "crack 256-bit key", "decrypt aes without key",
            "physical hardware rewrite", "hack remote server", "ddos"
        ]):
            return {
                "decision_category": CAT_H_NOT_FEASIBLE,
                "category_code": "H",
                "rationale": "The requested capability is physically impossible, unauthorized, or violates core safety guardrails.",
                "smallest_solution": "Reject request with transparent explanation of the constraint.",
                "target_component": None,
                "is_duplicate_prevented": False,
                "risk_level": "HIGH",
                "requires_approval": False,
                "can_execute": False
            }

        # 2. Category G: CONFIGURATION REQUIRED (Missing Keys/Permissions)
        if status == "PERMISSION_MISSING" or status == "EXISTS_UNCONFIGURED" or any(k in intent_lower for k in ["api key", "token", "credentials", "login", "authenticate"]):
            # Check if an existing tool merely needs an env var
            key_hints = [t for t in matched_tools if "key" in t.get("name", "").lower() or "token" in t.get("name", "").lower()]
            return {
                "decision_category": CAT_G_CONFIGURATION_REQUIRED,
                "category_code": "G",
                "rationale": "An implementation already exists but is missing required credentials or configuration settings.",
                "smallest_solution": "Provide configuration prompt or set environment variable.",
                "target_component": matched_tools[0]["name"] if matched_tools else "Environment Configuration",
                "is_duplicate_prevented": True,
                "risk_level": "LOW",
                "requires_approval": True,
                "can_execute": True
            }

        # 3. Category A: EXISTING FEATURE FIX
        if status == "EXISTS_BROKEN" or any(t.get("operational_status") in ["FAILING", "BROKEN"] for t in matched_tools):
            broken_tool = next((t for t in matched_tools if t.get("operational_status") in ["FAILING", "BROKEN"]), matched_tools[0] if matched_tools else None)
            target_name = broken_tool["name"] if broken_tool else "Unknown Tool"
            return {
                "decision_category": CAT_A_EXISTING_FEATURE_FIX,
                "category_code": "A",
                "rationale": f"An existing tool '{target_name}' is declared but failing. Repairing the existing handler is the smallest reliable solution.",
                "smallest_solution": f"Repair handler and exception paths in existing module for '{target_name}'.",
                "target_component": target_name,
                "is_duplicate_prevented": True,
                "risk_level": "MEDIUM",
                "requires_approval": True,
                "can_execute": True
            }

        # 4. Category B: EXISTING FEATURE UPGRADE
        # If an existing tool is a high match, prefer upgrading it rather than creating a duplicate!
        if matched_tools and (status == "EXISTS_PARTIAL" or any(k in intent_lower for k in ["improve", "upgrade", "enhance", "extend", "more"])):
            best_tool = matched_tools[0]
            if best_tool.get("relevance_score", 0) >= 1:
                return {
                    "decision_category": CAT_B_EXISTING_FEATURE_UPGRADE,
                    "category_code": "B",
                    "rationale": f"Existing tool '{best_tool['name']}' addresses the domain. Upgrading its arguments and execution handler avoids duplicate tools.",
                    "smallest_solution": f"Extend '{best_tool['name']}' with new options and parameters.",
                    "target_component": best_tool["name"],
                    "is_duplicate_prevented": True,
                    "risk_level": "MEDIUM",
                    "requires_approval": True,
                    "can_execute": True
                }

        # 5. Category E: NEW SKILL (Specialized high-level procedural workflow)
        skill_indicators = ["workflow", "guide", "procedure", "methodology", "prompt framework", "cheat sheet", "domain playbook", "best practices"]
        if any(si in intent_lower for si in skill_indicators):
            return {
                "decision_category": CAT_E_NEW_SKILL,
                "category_code": "E",
                "rationale": "The request is procedural knowledge, workflow guidelines, or prompt engineering best suited as a modular SKILL.md.",
                "smallest_solution": "Create a new standardized skill directory in .agents/skills with SKILL.md specification.",
                "target_component": f"skill_{abs(hash(user_request)) % 10000}",
                "is_duplicate_prevented": True,
                "risk_level": "MEDIUM",
                "requires_approval": True,
                "can_execute": True
            }

        # 6. Category F: NEW INTEGRATION (External API / SaaS service / MCP server)
        integration_indicators = ["integration", "webhook", "stripe", "slack", "shopify", "jira", "notion", "airtable", "salesforce", "mcp server"]
        if any(ii in intent_lower for ii in integration_indicators):
            return {
                "decision_category": CAT_F_NEW_INTEGRATION,
                "category_code": "F",
                "rationale": "The request requires interfacing with an external third-party API or protocol provider.",
                "smallest_solution": "Add dedicated API connector module or configure n8n webhook blueprint.",
                "target_component": f"connector_{abs(hash(user_request)) % 10000}",
                "is_duplicate_prevented": False,
                "risk_level": "MEDIUM",
                "requires_approval": True,
                "can_execute": True
            }

        # 7. Category D: NEW TOOL (Atomic reusable execution action)
        tool_indicators = ["tool", "function", "command", "utility", "script", "cli", "action"]
        if any(ti in intent_lower for ti in tool_indicators) or len(user_request.split()) <= 4:
            return {
                "decision_category": CAT_D_NEW_TOOL,
                "category_code": "D",
                "rationale": "A single reusable atomic action is required that does not exist in the 223 registered tools.",
                "smallest_solution": "Implement atomic tool handler and register in tool registry schema.",
                "target_component": f"tool_{abs(hash(user_request)) % 10000}",
                "is_duplicate_prevented": True,
                "risk_level": "MEDIUM",
                "requires_approval": True,
                "can_execute": True
            }

        # 8. Category C: NEW FEATURE (Subsystem or composite capability)
        return {
            "decision_category": CAT_C_NEW_FEATURE,
            "category_code": "C",
            "rationale": "No suitable implementation or tool exists. A new multi-step feature module is required.",
            "smallest_solution": "Implement dedicated feature module with associated test suite.",
            "target_component": f"feature_{abs(hash(user_request)) % 10000}",
            "is_duplicate_prevented": False,
            "risk_level": "MEDIUM",
            "requires_approval": True,
            "can_execute": True
        }


# Global Singleton Instance
upgrade_decision_engine = UpgradeDecisionEngine()
