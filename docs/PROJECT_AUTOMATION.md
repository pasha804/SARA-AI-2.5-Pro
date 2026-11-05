# SARA AI 2.5 PRO — AUTONOMOUS PROJECT MANAGEMENT SYSTEM

**System Component**: User Project Discovery, Auditing & Development Copilot  
**Module**: `sara_project_manager.py`  
**Registry Storage**: `data/project_registry.json`  
**Roots Scanned**: Configured workspace roots (`D:\MARAA AI`, `C:\Users\USER\Desktop`)  

---

## 1. Supported Stacks & Recognition Signatures

| Stack | Recognition Signature | Capabilities Enabled |
|---|---|---|
| **Next.js** | `package.json` with `next` dependency | Manifest check, script execution, build validation |
| **React / Vite** | `package.json` with `vite` / `react` | Linting, test running, dev server verification |
| **Electron** | `package.json` with `electron` | Single-instance checks, main/renderer script audit |
| **Python** | `requirements.txt`, `pyproject.toml`, `*.py` | Syntax validation, unittest execution, dependency checks |
| **HTML5 Vanilla** | `index.html` + `style.css` + `game.js` | Direct browser launch, DOM inspection |

---

## 2. Health Check & Scoring System

When Pasha Dev commands: *"SARA, mere projects ka audit karo"*:
1. SARA identifies all projects within workspace roots.
2. Performs non-destructive manifest inspection.
3. Computes a composite **Health Score (0-100)**:
   - High risk issues: -30 points (e.g. malformed `package.json`).
   - Warnings: -15 points (e.g. missing entry point).
   - Info: -5 points (e.g. missing test script).
4. Generates an executive summary and saves findings to `data/project_registry.json`.
