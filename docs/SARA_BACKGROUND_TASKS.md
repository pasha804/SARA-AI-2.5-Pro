# SARA AI 2.5 Pro — Background Task Execution Architecture

**Module**: `sara_task_manager.py`  
**State File**: `D:\MARAA AI\data\background_tasks.json`  
**Worker Pool**: Python `ThreadPoolExecutor` (Max 4 concurrent background threads)

---

## 1. Supported States & Transitions

Tasks progress through a deterministic, strictly validated finite state machine:

```
[QUEUED] ──────> [RUNNING] ──────> [COMPLETED]
   │                │
   ├─> [PAUSED] <───┤ (on pause / restart recovery)
   │      │         │
   │      └─────────┴──────> [FAILED] (on error / timeout)
   │
   ├─> [WAITING_APPROVAL] ───> [QUEUED] (upon Pasha Dev approval)
   │
   └───> [CANCELLED] (explicit cancel only)
```

1. **`QUEUED`**: Task is validated and waiting for an available worker thread.
2. **`RUNNING`**: Worker thread actively executing the task action.
3. **`PAUSED`**: Task temporarily suspended via explicit command or application restart recovery.
4. **`WAITING_APPROVAL`**: High-impact or destructive tasks (e.g. file deletion, process killing) awaiting explicit user confirmation.
5. **`COMPLETED`**: Action finished successfully; results stored in `result`.
6. **`FAILED`**: Action raised an unhandled exception or timed out; error logged in `error`.
7. **`CANCELLED`**: Explicitly terminated by user directive.

---

## 2. Core Resiliency Guarantees

### 2.1 Microphone & Voice Input Isolation Guarantee
- **Rule**: Passive microphone audio, room noise, or user speech turns **NEVER** automatically cancel, pause, or abort an active background task.
- **Enforcement**: Task state transitions require explicit programmatic method invocations (`pause_task()`, `cancel_task()`). Gemini Live voice turns process conversation independently from background task workers.

### 2.2 Restart Recovery
- If SARA restarts or the process stops unexpectedly while tasks are in `RUNNING` status, the startup sequence (`recover_interrupted_tasks()`) automatically detects the uncompleted tasks and safely transitions them to `PAUSED` with `error="Interrupted by application restart; safe resume available."`.

### 2.3 Duplicate Task Suppression
- Tasks are fingerprinted using a SHA-256 hash of their action and parameters. If an identical task is already in `QUEUED` or `RUNNING` state, the duplicate submission is suppressed, returning the existing active task handle.

### 2.4 Progress & Timeouts
- Tasks expose a numeric `progress` counter (0 to 100%).
- Worker lifecycle monitors elapsed execution time against `timeout_seconds`.

