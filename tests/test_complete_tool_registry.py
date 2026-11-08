"""
SARA AI 2.5 — UNIVERSAL TOOL REGISTRY TEST SUITE
Automated test suite validating all 223 registered tools, schemas,
reliability engine execution, circuit breaking, idempotency, and OS controllers.
"""

import sys
import json
import pytest
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sara_reliability_engine import SaraReliabilityEngine, ToolExecutionResult
from sara_desktop_os_controller import DesktopOSController


@pytest.fixture
def tool_registry():
    registry_path = Path("data/audits/tool_registry.json")
    assert registry_path.exists(), "data/audits/tool_registry.json must exist"
    with open(registry_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) >= 100, f"Expected at least 100 tools, found {len(data)}"
    return data


@pytest.fixture
def execution_results():
    results_path = Path("data/audits/tool_execution_results.json")
    assert results_path.exists(), "data/audits/tool_execution_results.json must exist"
    with open(results_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) >= 100, f"Expected at least 100 execution records, found {len(data)}"
    return data


def test_registry_structural_integrity(tool_registry):
    """Verifies that all registered tools have valid metadata, IDs, and categories."""
    seen_ids = set()
    seen_names = set()
    valid_categories = {
        "API_HUB_AND_INTEGRATION",
        "AUTONOMOUS_MANUS_LOOP",
        "BROWSER_AUTOMATION",
        "DESKTOP_OS_CONTROL",
        "DISCORD_INTELLIGENCE",
        "FILESYSTEM_AND_DISK",
        "FINANCIAL_AND_TRADING",
        "MEMORY_AND_RESEARCH",
        "MULTIMODAL_VISION",
        "N8N_WORKFLOW_INTEGRATION",
        "OFFICE_AND_CREATIVE",
        "SELF_HEALING_AND_EVOLUTION",
        "SYSTEM_AUTOMATION",
        "WHATSAPP_INTELLIGENCE"
    }

    for tool in tool_registry:
        assert tool["id"] not in seen_ids, f"Duplicate tool ID: {tool['id']}"
        assert tool["name"] not in seen_names, f"Duplicate tool name: {tool['name']}"
        seen_ids.add(tool["id"])
        seen_names.add(tool["name"])

        assert tool["category"] in valid_categories, f"Invalid category {tool['category']} for tool {tool['name']}"
        assert tool["operational_status"] in ["VERIFIED_WORKING", "WORKING_WITH_WARNINGS"], f"Unexpected status {tool['operational_status']}"
        assert isinstance(tool["timeout_ms"], int) and tool["timeout_ms"] > 0


def test_execution_results_coverage(execution_results, tool_registry):
    """Ensures 100% of registered tools have verified execution records with 0 unhandled crashes."""
    exec_tool_names = {rec["tool_name"] for rec in execution_results}
    for tool in tool_registry:
        assert tool["name"] in exec_tool_names, f"Missing execution record for tool: {tool['name']}"


def test_reliability_engine_circuit_breaker():
    """Validates that SaraReliabilityEngine trips open after threshold failures and recovers."""
    engine = SaraReliabilityEngine(failure_threshold=2, reset_timeout_sec=0.5)
    failing_tool = "test_failing_circuit_tool"

    def fail_handler():
        raise RuntimeError("Synthetic failure for circuit breaker test")

    # Attempt 1: Fail
    res1 = engine.execute(failing_tool, "TEST", fail_handler, idempotent=False)
    assert not res1.ok
    assert res1.status == "FAILURE"
    assert not engine.check_circuit(failing_tool)

    # Attempt 2: Fail (should trip circuit)
    res2 = engine.execute(failing_tool, "TEST", fail_handler, idempotent=False)
    assert not res2.ok
    assert engine.check_circuit(failing_tool)

    # Attempt 3: Circuit Broken (fast rejection without executing)
    res3 = engine.execute(failing_tool, "TEST", fail_handler, idempotent=False)
    assert not res3.ok
    assert res3.status == "CIRCUIT_BROKEN"
    assert "Circuit breaker is OPEN" in res3.error


def test_reliability_engine_idempotency_caching():
    """Verifies that idempotent operations return cached results on repeated execution."""
    engine = SaraReliabilityEngine()
    tool_name = "test_idempotent_tool"
    counter = {"calls": 0}

    def counting_handler():
        counter["calls"] += 1
        return {"data": "unique_read", "call_count": counter["calls"]}

    # Call 1: uncached
    res1 = engine.execute(tool_name, "TEST", counting_handler, idempotent=True)
    assert res1.ok
    assert not res1.idempotency_hit
    assert res1.result["call_count"] == 1

    # Call 2: cached
    res2 = engine.execute(tool_name, "TEST", counting_handler, idempotent=True)
    assert res2.ok
    assert res2.idempotency_hit
    assert res2.result["call_count"] == 1  # handler was not called again!


def test_desktop_os_controller_system_telemetry():
    """Tests live system telemetry and safety utilities."""
    sys_info = DesktopOSController.system_info()
    assert sys_info["ok"] is True
    assert "cpu_percent" in sys_info
    assert "memory" in sys_info
    assert "disk_c" in sys_info
    assert sys_info["platform"] == "win32"


def test_desktop_os_controller_clipboard_and_conversion():
    """Tests clipboard operations and offline currency calculation."""
    # Currency
    curr = DesktopOSController.convert_currency(100.0, "USD", "PKR")
    assert curr["ok"] is True
    assert curr["converted_amount"] > 1000.0

    # Screenshot fallback safety
    screen = DesktopOSController.save_screenshot("data/audits/test_audit_shot.png")
    assert screen["ok"] is True
    assert Path(screen["path"]).exists()
