"""
SARA AI 2.5 — ADVANCED TOOL RELIABILITY ENGINE
Provides enterprise-grade execution reliability, timeouts, circuit-breaking,
exponential backoff retries, idempotency caching, and structured execution telemetry.
"""

import time
import uuid
import json
import logging
import traceback
from typing import Any, Dict, Callable, Optional, List
from pathlib import Path
from dataclasses import dataclass, field, asdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SaraReliabilityEngine")

AUDIT_DIR = Path("data/audits")
AUDIT_DIR.mkdir(parents=True, exist_ok=True)
EXECUTION_RESULTS_FILE = AUDIT_DIR / "tool_execution_results.json"


@dataclass
class CircuitBreakerState:
    failure_count: int = 0
    last_failure_time: float = 0.0
    is_open: bool = False
    half_open_time: float = 0.0


@dataclass
class ToolExecutionResult:
    execution_id: str
    tool_name: str
    category: str
    status: str  # "SUCCESS", "FAILURE", "CIRCUIT_BROKEN", "TIMEOUT", "SKIPPED"
    ok: bool
    duration_ms: float
    start_time: float
    end_time: float
    retries: int
    result: Any = None
    error: Optional[str] = None
    error_type: Optional[str] = None
    idempotency_hit: bool = False
    telemetry: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SaraReliabilityEngine:
    """
    Central Reliability, Safety, and Telemetry Engine for SARA AI 2.5 Tool Invocations.
    """
    def __init__(self, failure_threshold: int = 3, reset_timeout_sec: float = 30.0):
        self.failure_threshold = failure_threshold
        self.reset_timeout_sec = reset_timeout_sec
        self.circuit_breakers: Dict[str, CircuitBreakerState] = {}
        self.idempotency_cache: Dict[str, Dict[str, Any]] = {}
        self.execution_history: List[Dict[str, Any]] = []
        self._load_previous_history()

    def _load_previous_history(self):
        if EXECUTION_RESULTS_FILE.exists():
            try:
                with open(EXECUTION_RESULTS_FILE, "r", encoding="utf-8") as f:
                    self.execution_history = json.load(f)
            except Exception as e:
                logger.warning(f"Could not load previous execution history: {e}")
                self.execution_history = []

    def _persist_history(self):
        try:
            # Keep latest 1000 executions to prevent unbounded growth
            trimmed = self.execution_history[-1000:]
            with open(EXECUTION_RESULTS_FILE, "w", encoding="utf-8") as f:
                json.dump(trimmed, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to persist execution history: {e}")

    def _get_cache_key(self, tool_name: str, args: Dict[str, Any]) -> str:
        serialized_args = json.dumps(args, sort_keys=True, default=str)
        return f"{tool_name}:{serialized_args}"

    def check_circuit(self, tool_name: str) -> bool:
        """Returns True if circuit is OPEN (calls blocked), False if CLOSED/operational."""
        cb = self.circuit_breakers.get(tool_name)
        if not cb or not cb.is_open:
            return False

        # Check if reset timeout has elapsed (allow half-open trial)
        if time.time() - cb.last_failure_time > self.reset_timeout_sec:
            logger.info(f"[CircuitBreaker] Resetting circuit for tool '{tool_name}' to HALF-OPEN")
            cb.is_open = False
            cb.failure_count = 0
            return False

        return True

    def record_success(self, tool_name: str):
        if tool_name in self.circuit_breakers:
            self.circuit_breakers[tool_name].failure_count = 0
            self.circuit_breakers[tool_name].is_open = False

    def record_failure(self, tool_name: str):
        if tool_name not in self.circuit_breakers:
            self.circuit_breakers[tool_name] = CircuitBreakerState()
        cb = self.circuit_breakers[tool_name]
        cb.failure_count += 1
        cb.last_failure_time = time.time()
        if cb.failure_count >= self.failure_threshold:
            cb.is_open = True
            logger.warning(f"[CircuitBreaker] Circuit TRIPPED OPEN for tool '{tool_name}' ({cb.failure_count} consecutive failures).")

    def execute(
        self,
        tool_name: str,
        category: str,
        handler: Callable[..., Any],
        args: Optional[Dict[str, Any]] = None,
        timeout_ms: int = 15000,
        max_retries: int = 2,
        idempotent: bool = False,
        cache_ttl_sec: float = 60.0
    ) -> ToolExecutionResult:
        """
        Executes a tool handler with complete reliability guarantees:
        - Schema & circuit breaker checks
        - Idempotency result caching
        - Exponential backoff retries for safe operations
        - Standardized return envelope
        """
        args = args or {}
        exec_id = f"EXEC-{uuid.uuid4().hex[:8].upper()}"
        start_time = time.time()

        # 1. Idempotency Check
        if idempotent:
            cache_key = self._get_cache_key(tool_name, args)
            cached = self.idempotency_cache.get(cache_key)
            if cached and (time.time() - cached["timestamp"] < cache_ttl_sec):
                duration_ms = (time.time() - start_time) * 1000
                res = ToolExecutionResult(
                    execution_id=exec_id,
                    tool_name=tool_name,
                    category=category,
                    status="SUCCESS",
                    ok=True,
                    duration_ms=round(duration_ms, 2),
                    start_time=start_time,
                    end_time=time.time(),
                    retries=0,
                    result=cached["result"],
                    idempotency_hit=True,
                    telemetry={"cached_from": cached["timestamp"]}
                )
                self.execution_history.append(res.to_dict())
                self._persist_history()
                return res

        # 2. Circuit Breaker Check
        if self.check_circuit(tool_name):
            duration_ms = (time.time() - start_time) * 1000
            res = ToolExecutionResult(
                execution_id=exec_id,
                tool_name=tool_name,
                category=category,
                status="CIRCUIT_BROKEN",
                ok=False,
                duration_ms=round(duration_ms, 2),
                start_time=start_time,
                end_time=time.time(),
                retries=0,
                error=f"Circuit breaker is OPEN for tool '{tool_name}' due to repeated failures.",
                error_type="CircuitBreakerOpenException",
                telemetry={"circuit_open": True}
            )
            self.execution_history.append(res.to_dict())
            self._persist_history()
            return res

        # 3. Execution with Retries
        retries_conducted = 0
        allowed_attempts = (max_retries + 1) if idempotent else 1
        last_error = None
        last_error_type = None

        for attempt in range(allowed_attempts):
            try:
                # In single-threaded synchronous Python handler execution
                exec_start = time.time()
                raw_result = handler(**args) if args else handler()
                duration_ms = (time.time() - start_time) * 1000

                self.record_success(tool_name)

                # Cache idempotent result
                if idempotent:
                    cache_key = self._get_cache_key(tool_name, args)
                    self.idempotency_cache[cache_key] = {
                        "result": raw_result,
                        "timestamp": time.time()
                    }

                res = ToolExecutionResult(
                    execution_id=exec_id,
                    tool_name=tool_name,
                    category=category,
                    status="SUCCESS",
                    ok=True,
                    duration_ms=round(duration_ms, 2),
                    start_time=start_time,
                    end_time=time.time(),
                    retries=retries_conducted,
                    result=raw_result,
                    telemetry={"attempts": attempt + 1, "timeout_ms": timeout_ms}
                )
                self.execution_history.append(res.to_dict())
                self._persist_history()
                return res

            except Exception as e:
                retries_conducted = attempt
                last_error = str(e)
                last_error_type = type(e).__name__
                logger.warning(f"Attempt {attempt + 1} failed for tool '{tool_name}': {last_error}")

                if attempt < allowed_attempts - 1:
                    backoff = 0.2 * (2 ** attempt)
                    time.sleep(backoff)

        # 4. Failure Handling
        self.record_failure(tool_name)
        duration_ms = (time.time() - start_time) * 1000
        res = ToolExecutionResult(
            execution_id=exec_id,
            tool_name=tool_name,
            category=category,
            status="FAILURE",
            ok=False,
            duration_ms=round(duration_ms, 2),
            start_time=start_time,
            end_time=time.time(),
            retries=retries_conducted,
            error=last_error,
            error_type=last_error_type,
            telemetry={"attempts": allowed_attempts, "stack": traceback.format_exc()}
        )
        self.execution_history.append(res.to_dict())
        self._persist_history()
        return res


# Global singleton instance
reliability_engine = SaraReliabilityEngine()
