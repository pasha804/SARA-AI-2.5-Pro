# SARA AI 2.5 PRO — SECURITY, AUTONOMY & PERMISSIONS REGISTRY

**Document Version**: 2.5.0-PRO  
**Owner & Creator**: Muhammad Mubashar (Pasha Dev)  

---

## 1. Three-Tier Risk & Permission Architecture

SARA operates under an explicit, risk-calibrated permission model that balances deep engineering autonomy with operating system safety.

### Level 1: Low-Risk Actions (Autonomous Execution)
SARA executes these actions autonomously without interrupting Pasha Dev with redundant confirmation prompts:
- Reading project files, manifests, and documentation within authorized workspace roots.
- Creating requested files, directories, scripts, and tests.
- Editing existing source files for authorized development tasks.
- Running unit tests, linters, syntax checks, and standard build scripts.
- Launching recognized local applications (VS Code, Cursor, Chrome, WhatsApp Desktop, Explorer).
- Ingesting Google News RSS feeds and scraping public web articles silently.
- Displaying holographic HUD intelligence overlays on screen.

### Level 2: Moderate-Risk Actions (Audit-Logged)
Logged to `data/activity_audit.log` with execution safeguards:
- Installing npm or pip dependencies.
- Modifying local environment configurations or port bindings.
- Executing long-running background subprocesses (bound to 15s-30s timeouts).

### Level 3: High-Impact Actions (Mandatory Confirmation Gate)
Strictly gated behind the `confirmPendingAction` verification token:
- Permanently deleting files or directories (`deleteFile`).
- Rebooting or shutting down the Windows workstation (`requestPowerAction`).
- Destructive Git operations (e.g. `git reset --hard`, `git push --force`).
- Modifying Windows Registry keys outside SARA's auto-start entry.
