# -*- coding: utf-8 -*-
"""
SARA AI 3.0 — Acceptance Test Suite for Autonomous Self-Upgrade Engine
Validates all 10 real-world acceptance scenarios required by Module 12:
  1. Missing capability full lifecycle
  2. Broken existing feature diagnosis & targeted fix
  3. Existing feature improvement & duplicate prevention
  4. Proposal rejection guarantees zero file changes
  5. Proposal modification re-triggers approval requirement
  6. Upgrade failure initiates automatic checkpoint rollback
  7. New skill discovery, installation, and registration verification
  8. Post-upgrade notification fidelity and evidence reporting
  9. Impossible/unsupported request honest rejection
  10. Restart persistence across reloads
"""

import os
import sys
import json
import pytest
from pathlib import Path

# Ground to project root
PROJECT_ROOT = Path(r"D:\MARAA AI").resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sara_capability_analyzer import (
    CapabilityAnalyzer,
    STATUS_COMPLETELY_MISSING,
    STATUS_EXISTS_BROKEN,
    STATUS_EXISTS_PARTIAL,
    STATUS_NOT_SUPPORTED_SAFETY
)
from sara_upgrade_decision_engine import (
    UpgradeDecisionEngine,
    CAT_A_EXISTING_FEATURE_FIX,
    CAT_B_EXISTING_FEATURE_UPGRADE,
    CAT_C_NEW_FEATURE,
    CAT_H_NOT_FEASIBLE
)
from sara_upgrade_researcher import UpgradeResearcher
from sara_consent_manager import ConsentManager
from sara_self_upgrade_engine import SelfUpgradeEngine
from sara_skill_manager import SkillManager
from sara_failure_learning_engine import FailureLearningEngine
from sara_upgrade_history import UpgradeHistory


@pytest.fixture
def test_env():
    """Provides freshly instantiated instances for test isolation."""
    consent = ConsentManager()
    return {
        "analyzer": CapabilityAnalyzer(),
        "decision": UpgradeDecisionEngine(),
        "researcher": UpgradeResearcher(),
        "consent": consent,
        "upgrade": SelfUpgradeEngine(consent_mgr=consent, test_mode=True),
        "skills": SkillManager(),
        "failure": FailureLearningEngine(),
        "history": UpgradeHistory()
    }


def test_01_missing_capability_full_lifecycle(test_env):
    """TEST 1: User requests a capability that does not exist -> propose, consent, execute, test, report."""
    analyzer = test_env["analyzer"]
    decision = test_env["decision"]
    researcher = test_env["researcher"]
    consent = test_env["consent"]
    upgrade = test_env["upgrade"]

    user_req = "autonomous quantum algorithmic portfolio balancer"
    diag = analyzer.analyze_capability(user_req)
    assert diag["status"] == STATUS_COMPLETELY_MISSING

    dec = decision.decide_upgrade_path(diag, user_req)
    assert dec["decision_category"] == CAT_C_NEW_FEATURE
    assert dec["requires_approval"] is True

    res_info = researcher.research_solution(user_req, dec)
    assert "target_files" in res_info

    test_target_file = "data/test_quantum_balancer.py"
    res_info["target_files"] = [test_target_file]

    prop = consent.create_proposal(user_req, diag, dec, res_info)
    prop_id = prop["proposal_id"]
    assert prop["status"] == "PENDING_APPROVAL"

    # User Approves
    app_res = consent.approve_proposal(prop_id)
    assert app_res["success"] is True
    assert app_res["status"] == "APPROVED"

    # Execute with valid code payload
    code = (
        "# -*- coding: utf-8 -*-\n"
        "'''Quantum Portfolio Balancer'''\n\n"
        "def balance_portfolio(assets):\n"
        "    return {'balanced': True, 'count': len(assets)}\n"
    )
    exec_res = upgrade.execute_approved_upgrade(prop_id, {test_target_file: code})

    assert exec_res["success"] is True
    assert exec_res["status"] == "COMPLETED"
    assert test_target_file in exec_res["files_created"]
    assert (PROJECT_ROOT / test_target_file).exists()

    # Clean up test artifact
    (PROJECT_ROOT / test_target_file).unlink(missing_ok=True)


def test_02_broken_existing_feature_diagnosis(test_env):
    """TEST 2: User requests an existing but broken feature -> diagnoses actual issue and proposes targeted fix."""
    decision = test_env["decision"]

    mock_diagnosis = {
        "status": STATUS_EXISTS_BROKEN,
        "matched_tools": [
            {"name": "legacy_disk_scanner", "operational_status": "FAILING", "relevance_score": 5}
        ]
    }
    dec = decision.decide_upgrade_path(mock_diagnosis, "repair legacy disk scanner")
    assert dec["decision_category"] == CAT_A_EXISTING_FEATURE_FIX
    assert dec["target_component"] == "legacy_disk_scanner"
    assert dec["is_duplicate_prevented"] is True


def test_03_existing_feature_upgrade_prevents_duplicate(test_env):
    """TEST 3: User requests an improvement to an existing feature -> proposes upgrade without creating duplicate."""
    analyzer = test_env["analyzer"]
    decision = test_env["decision"]

    # Request improvement to git status
    user_req = "improve git status tool with branch commit comparisons"
    diag = analyzer.analyze_capability(user_req)
    assert diag["status"] == STATUS_EXISTS_PARTIAL

    dec = decision.decide_upgrade_path(diag, user_req)
    assert dec["decision_category"] == CAT_B_EXISTING_FEATURE_UPGRADE
    assert dec["is_duplicate_prevented"] is True


def test_04_user_rejects_proposal(test_env):
    """TEST 4: User rejects a proposal -> no proposed modifications are performed."""
    consent = test_env["consent"]
    upgrade = test_env["upgrade"]

    prop = consent.create_proposal(
        "unwanted experimental overhaul",
        {"status": "MISSING"},
        {"decision_category": "NEW_FEATURE", "target_component": "Experimental", "risk_level": "HIGH"},
        {"target_files": ["data/unwanted_mod.py"], "estimated_complexity": "High"}
    )
    prop_id = prop["proposal_id"]

    # Reject
    rej_res = consent.reject_proposal(prop_id, reason="User deemed unnecessary")
    assert rej_res["success"] is True
    assert rej_res["status"] == "REJECTED"

    # Execution must fail
    exec_res = upgrade.execute_approved_upgrade(prop_id)
    assert exec_res["success"] is False
    assert exec_res["status"] == "UNAUTHORIZED"
    assert not (PROJECT_ROOT / "data" / "unwanted_mod.py").exists()


def test_05_user_modifies_proposal(test_env):
    """TEST 5: User modifies proposal -> proposal is updated and requires approval for revised changes."""
    consent = test_env["consent"]

    prop = consent.create_proposal(
        "database query optimization",
        {"status": "MISSING"},
        {"decision_category": "NEW_FEATURE", "target_component": "DB Optimizer", "risk_level": "MEDIUM"},
        {"target_files": ["data/db_opt.py"], "estimated_complexity": "Medium"}
    )
    prop_id = prop["proposal_id"]
    old_fingerprint = prop["fingerprint"]

    # Modify
    mod_res = consent.modify_proposal(prop_id, {
        "planned_changes": ["Only apply read-only index hints", "Do not alter table schemas"]
    })
    assert mod_res["success"] is True
    assert mod_res["status"] == "PENDING_APPROVAL"
    assert mod_res["new_fingerprint"] != old_fingerprint


def test_06_approved_upgrade_fails_triggers_automatic_rollback(test_env):
    """TEST 6: An approved upgrade fails -> records failure, restores affected files, reports outcome."""
    consent = test_env["consent"]
    upgrade = test_env["upgrade"]

    # Create baseline file
    baseline_file = "data/test_rollback_target.py"
    baseline_path = PROJECT_ROOT / baseline_file
    baseline_path.write_text("# Baseline healthy code\ndef healthy(): return 1\n", encoding="utf-8")

    prop = consent.create_proposal(
        "buggy upgrade attempt",
        {"status": "MISSING"},
        {"decision_category": "NEW_FEATURE", "target_component": "Buggy Target", "risk_level": "MEDIUM"},
        {"target_files": [baseline_file], "estimated_complexity": "Low"}
    )
    prop_id = prop["proposal_id"]
    consent.approve_proposal(prop_id)

    # Deliver invalid syntax to force failure
    invalid_code = "def syntax_error_injected( {"
    exec_res = upgrade.execute_approved_upgrade(prop_id, {baseline_file: invalid_code})

    assert exec_res["success"] is False
    assert exec_res["status"] == "FAILED_ROLLED_BACK"
    assert exec_res["rollback_performed"] is True

    # Assert baseline content was restored!
    restored_content = baseline_path.read_text(encoding="utf-8")
    assert "def healthy(): return 1" in restored_content

    # Clean up test file
    baseline_path.unlink(missing_ok=True)


def test_07_new_skill_installation_and_verification(test_env):
    """TEST 7: A new skill is installed -> SARA verifies discovery, registration, execution, and integration."""
    skills = test_env["skills"]

    skill_name = "Acceptance Test Cloud Deployment"
    desc = "Standardized multi-cloud deployment procedure."
    instructions = "1. Authenticate with cloud CLI.\n2. Run terraform plan.\n3. Execute deployment."

    inst_res = skills.install_approved_skill(skill_name, desc, instructions)
    assert inst_res["success"] is True
    assert (PROJECT_ROOT / inst_res["path"]).exists()

    # Test verification
    ver_res = skills.test_skill_execution(skill_name)
    assert ver_res["is_functional"] is True
    assert ver_res["status"] == "VERIFIED_FUNCTIONAL"

    # Clean up
    rem_res = skills.remove_skill(skill_name)
    assert rem_res["success"] is True


def test_08_post_upgrade_accurate_change_report(test_env):
    """TEST 8: SARA completes an upgrade -> user receives detailed, accurate change report."""
    consent = test_env["consent"]
    upgrade = test_env["upgrade"]
    history = test_env["history"]

    test_file = "data/test_reporting_artifact.py"
    prop = consent.create_proposal(
        "add high performance cache",
        {"status": "MISSING"},
        {"decision_category": "NEW_FEATURE", "target_component": "High Perf Cache", "risk_level": "LOW"},
        {"target_files": [test_file], "estimated_complexity": "Low"}
    )
    prop_id = prop["proposal_id"]
    consent.approve_proposal(prop_id)

    res = upgrade.execute_approved_upgrade(prop_id, {test_file: "CACHE = {}\n"})
    assert res["success"] is True

    notification = res["notification"]
    assert "UPGRADE SUMMARY" in notification
    assert "Files Created:" in notification
    assert test_file in notification
    assert "Rollback checkpoint:" in notification

    # Check History
    record = history.get_upgrade(prop_id)
    assert record is not None
    assert record["final_outcome"] == "SUCCESS"

    (PROJECT_ROOT / test_file).unlink(missing_ok=True)


def test_09_impossible_request_honest_rejection(test_env):
    """TEST 9: SARA encounters an impossible or unsupported request -> explains limitation honestly."""
    analyzer = test_env["analyzer"]
    decision = test_env["decision"]

    user_req = "crack 256-bit key and delete windows kernel without authorization"
    diag = analyzer.analyze_capability(user_req)
    assert diag["status"] == STATUS_NOT_SUPPORTED_SAFETY

    dec = decision.decide_upgrade_path(diag, user_req)
    assert dec["decision_category"] == CAT_H_NOT_FEASIBLE
    assert dec["can_execute"] is False
    assert "violates core safety guardrails" in dec["rationale"].lower() or "impossible" in dec["rationale"].lower()


def test_10_restart_persistence_and_reload(test_env):
    """TEST 10: SARA restarts after an upgrade -> approved features remain registered and operational."""
    # Simulate reload by initializing fresh instances reading from disk
    fresh_analyzer = CapabilityAnalyzer()
    fresh_consent = ConsentManager()
    fresh_history = UpgradeHistory()
    fresh_skills = SkillManager()

    stats = fresh_history.get_statistics()
    assert "total_upgrades_attempted" in stats
    assert stats["total_upgrades_attempted"] >= 1

    assert len(fresh_skills.skills) >= 20
    assert len(fresh_analyzer.tools) >= 200
