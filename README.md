# 🌌 SARA AI 3.0 Enterprise Pro — Autonomous Self-Upgrading Workstation Agent & 3D Living Companion

<p align="center">
  <img src="sara_official_icon.png" alt="SARA AI 3.0 Enterprise Pro" width="170" />
</p>

<p align="center">
  <a href="https://github.com/pasha804/SARA-AI-2.5-Pro"><img src="https://img.shields.io/badge/Version-3.0_Enterprise_Pro-8b5cf6?style=for-the-badge&logo=electron" alt="Version 3.0 Enterprise Pro" /></a>
  <img src="https://img.shields.io/badge/Python-3.14%20%7C%203.12-38bdf8?style=for-the-badge&logo=python" alt="Python 3.14" />
  <img src="https://img.shields.io/badge/Tests-47%2F47%20Green-10b981?style=for-the-badge&logo=pytest" alt="47/47 Tests Passed" />
  <img src="https://img.shields.io/badge/System%20Health-100.0%25%20Verified-10b981?style=for-the-badge&logo=checkmarx" alt="System Health 100%" />
  <img src="https://img.shields.io/badge/Core%20Tools-223%20Verified-06b6d4?style=for-the-badge" alt="223 Verified Tools" />
  <img src="https://img.shields.io/badge/Automations-439%20Cataloged-f59e0b?style=for-the-badge&logo=n8n" alt="439 Automations" />
  <img src="https://img.shields.io/badge/Self--Upgrade-10%2F10%20Tests%20Passed-ec4899?style=for-the-badge" alt="Self-Upgrade Engine" />
  <a href="https://github.com/pasha804"><img src="https://img.shields.io/badge/Maintainer-@pasha804-10b981?style=for-the-badge&logo=github" alt="pasha804" /></a>
  <img src="https://img.shields.io/badge/License-MIT-success?style=for-the-badge" alt="MIT License" />
</p>

---

## 🌟 Executive Overview

**SARA AI 3.0 Enterprise Pro** (*Synthetic Autonomous Reasoning Avatar*) is an elite multimodal desktop AI companion, autonomous software engineer, and self-expanding workstation operating system. 

Unlike traditional LLM wrappers that merely respond *"I cannot do this"* when encountering unsupported tasks, **SARA 3.0 autonomously detects its own limitations, diagnoses structural root causes, formulates cryptographically fingerprinted upgrade proposals, requests explicit human consent, applies minimal-diff code or skill upgrades, runs regression verification, and automatically rolls back within 500ms if verification fails.**

Combined with an interactive **Three.js 60 FPS 3D living avatar**, native **Windows Win32 OS control (2.4ms latency)**, resilient **Playwright browser autonomy with 5-tier locators**, strict **NEXORA Discord community operations**, and a massive ecosystem of **439 enterprise automations**, SARA AI 3.0 represents a breakthrough in autonomous agent engineering.

---

## 🏛️ System Architecture Topology

```mermaid
graph TD
    User([👤 User / Pasha Jan]) <--> UI[🖥️ Electron 3D Viewport & Cybernetic HUD :3344]
    UI <--> Router[⚡ Fast-Path Native Node.js Dispatcher server.cjs]
    Router <--> Brain[🧠 SARA Neural Brain Engine sara_neural_brain.py]
    
    subgraph COGNITIVE_CORE ["Cognitive Core & Expansion Layer"]
        Brain <--> APInex[🌐 APInex Multi-Model Provider glm-5.3 / deepseek-v4 / gemini-3.8]
        Brain <--> Memory[💾 3-Tier SQLite & FTS5 Long-Term Memory Engine]
        Brain <--> SelfUpgrade[🚀 Autonomous Self-Upgrade & Decision Engine A-H]
        Brain <--> SelfHealing[🛡️ AST Anomaly Diagnosis & 500ms Rollback Engine]
    end

    subgraph WORKSPACE_EXECUTION ["Workstation Automation & Execution Engines"]
        Router <--> NativeOS[⚡ Direct Win32 Desktop OS Controller 2.4ms avg]
        Router <--> BrowserEngine[🌐 Autonomous Playwright Engine 5-Tier Locators]
        Router <--> DiscordMgr[🎮 NEXORA Discord Community Manager 59 Channels]
        Router <--> AutomationSuite[🔄 439 Automations: 415 n8n + 24 Native Pipelines]
        Router <--> ManusLoop[🔄 OpenManus Autonomous Task & Artifact Loop]
        Router <--> AntigravityBridge[🛸 Google Antigravity IDE Bridge agy.exe]
    end
```

---

## 🚀 Key Engineering Pillars

### 1. 🚀 Autonomous Self-Upgrade & Capability Expansion Engine (v3.0 Core)
SARA 3.0 introduces a closed-loop self-expansion architecture governing 10 specialized modules:
- **Capability Analyzer (`sara_capability_analyzer.py`)**: Forensically audits 223 tools and 439 automations to classify requests into `EXISTS_FUNCTIONAL`, `EXISTS_BROKEN`, `EXISTS_PARTIAL`, `EXISTS_UNCONFIGURED`, `PERMISSION_MISSING`, `COMPLETELY_MISSING`, or `NOT_SUPPORTED_SAFETY`.
- **Decision Engine (`sara_upgrade_decision_engine.py`)**: Enforces the **Smallest Reliable Solution Rule** across 8 deterministic categories:
  - `Cat A (EXISTING_FEATURE_FIX)`: In-place handler and exception repair.
  - `Cat B (EXISTING_FEATURE_UPGRADE)`: Extends existing module parameters — **zero duplicate tools**.
  - `Cat C (NEW_FEATURE)`: Multi-step dedicated Python subsystem.
  - `Cat D (NEW_TOOL)`: Atomic reusable action registered in tool registry.
  - `Cat E (NEW_SKILL)`: Declarative YAML frontmatter skill in `.agents/skills/`.
  - `Cat F (NEW_INTEGRATION)`: API connector or n8n webhook integration.
  - `Cat G (CONFIGURATION_REQUIRED)`: Missing environment credentials / API token prompt.
  - `Cat H (NOT_FEASIBLE)`: Transparent rejection of physically impossible or unsafe requests.
- **Cryptographic Consent Gate (`sara_consent_manager.py`)**: Computes a SHA-256 fingerprint of `feature|files|planned_steps`. Explicit approval is bound strictly to that proposal ID; generic past approvals cannot authorize future modifications.
- **Pre-Upgrade Snapshots & Rollback (`sara_self_upgrade_engine.py`)**: Creates immutable file backups in `data/backups/upgrades/{prop_id}/`. Validates Python AST syntax (`ast.parse()`) and capability test suites. Reverts changes automatically within 500ms on failure.
- **Autonomous Skill Manager (`sara_skill_manager.py`)**: Audits skills against malicious shell injection (`rm -rf`, `powershell -enc`, `curl | sh`), installs valid `SKILL.md` specifications, and verifies runtime discovery.
- **Permanent History Ledger (`sara_upgrade_history.py`)**: Immutable, searchable audit trail in `data/audits/upgrade_history.json` with regex redaction of secrets, tokens, and keys.

```mermaid
flowchart LR
    Limitation["Task Limitation"] --> Diag["Forensic Diagnosis"]
    Diag --> Classify["Classify (Cat A-H)"]
    Classify --> Research["Grounded Research"]
    Research --> Consent["Signed Consent Gate"]
    Consent --> Snapshot["Pre-Upgrade Snapshot"]
    Snapshot --> Implement["Minimal Diff Code"]
    Implement --> Verify{"AST & Tests Pass?"}
    Verify -->|"YES"| Commit["Finalize & Report"]
    Verify -->|"NO"| Rollback["Auto-Rollback (<500ms)"]
```

---

### 2. ⚡ Direct Native Windows Desktop OS Controller (`sara_desktop_os_controller.py`)
- **Port 8765 Deprecation**: Completely eliminated legacy background agent polling on `http://127.0.0.1:8765`, reducing OS action latency from **20,000ms timeout down to 2.4ms average (~8,333x faster)**.
- **Win32 & PyAutoGUI Core**: Direct in-process mouse clicking, double clicking, smooth cursor movement, text typing, keyboard hotkeys, and window management (`minimize`, `maximize`, `close`, `active_window`).
- **Clipboard & Telemetry**: Native clipboard read/write/clear, real-time CPU, RAM, Disk, Battery, and Uptime queries without external process overhead.
- **Safe Power Management**: Windows shutdown, restart, sleep, and lock operations gated with strict dry-run confirmation guards.

---

### 3. 🌐 Autonomous Resilient Playwright Browser Engine (`sara_interactive_browser.py`)
- **5-Tier Fallback Locator Hierarchy**:
  $$\text{CSS / XPath} \longrightarrow \text{ID / Name} \longrightarrow \text{ARIA / Label} \longrightarrow \text{Placeholder / Test-ID} \longrightarrow \text{Visible Text}$$
- **Dynamic Single Page Applications (SPAs)**: Robust handling of reactive DOM state mutations, select dropdowns, textareas, and natural mouse scrolling.
- **Cookie Banner Auto-Dismissal**: Parallel 300ms race against intrusive GDPR and cookie prompts to ensure uninterrupted autonomous navigation.
- **Multi-Tab Context Management**: Autonomously opens (`new_tab`), lists (`list_tabs`), switches (`switch_tab`), and cleans up (`close_tab`) tabs across persistent sessions.
- **Persistent Profiles**: Preserves authentication and local storage in `data/browser_sessions/sara_default_profile`.

---

### 4. 🌸 3D Live Avatar, Audio Synthesizer & Cockpit Hub
- **Interactive Three.js Viewport**: Real-time 60 FPS rendering of Evelyn PMX / GLB 3D model with customized holographic cybernetic shader room.
- **Web Audio FFT Phoneme Extraction**: Real-time viseme lip-sync (`v_aa`, `v_ih`, `v_ou`, `v_ee`, `v_oh`) synchronizing mouth morphs to synthesized audio.
- **Procedural Audio Synthesizer**: Native zero-asset audio synthesis generating futuristic cybernetic auditory feedback on micro-interactions.
- **4-in-1 Command Cockpit Modal**: Comprehensive UI control center for Workspaces, 439 Automations, NEXORA Discord, and APInex model selection.

---

### 5. 🎮 NEXORA Discord Community Operator (`sara_automation_suite.py`)
- **Strict Server Whitelist Lock**: Hardcoded server validation enforcing isolation strictly to **`NEXORA` (Guild ID `1430932596956270634`)**. Foreign interactions are rejected and logged as security violations.
- **Full 59-Channel Topology Mapped**:
  | Category | Channels |
  |---|---|
  | **VOICE CHANNELS (5)** | `General VC`, `-study-room`, `Coding VC`, `Pair Programming`, `Events Stage` |
  | **INFORMATION (4)** | `-rules`, `-announcements`, `-introductions`, `-server-goals` |
  | **COMMUNITY (4)** | `-general-chat`, `-random-chat`, `-daily-wins`, `-help-and-support` |
  | **DEVELOPMENT (26)** | `-python`, `-java`, `-javascript`, `-typescript`, `-react`, `-nodejs`, `-web-development`, `-app-development`, `-ai-ml`, `-data-science`, `-database`, `-backend`, `-frontend`, `-devops`, `-linux`, `-cybersecurity`, `-game-development`, `-c-language`, `-cpp`, `-csharp`, `-swift-ios`, `-android-development`, `-cloud-computing`, `-api-development`, `-testing-qa`, `-tools-and-tech` |
  | **PROJECTS (4)** | `-project-showcase`, `-portfolio-review`, `-open-source`, `-build-in-public` |
  | **COLLABORATION (4)** | `-find-teammates`, `-freelancing`, `-hackathons`, `-looking-for-help` |
  | **LEARNING HUB (6)** | `-study-resources`, `-learning-roadmaps`, `-coding-challenges`, `-interview-prep`, `-certifications`, `-ask-a-mentor` |
  | **CAREERS (6)** | `-job-opportunities`, `-remote-jobs`, `-internships`, `-resume-review`, `-mock-interviews`, `-freelancing-tips` |
- **Safe Simulation Mode**: Headless test runs employ `simulate=True` to prevent accidental broadcast of unauthorized test payloads.

---

### 6. 🔄 439 Enterprise Automations & 223 Core Tools
- **415 n8n Workflow Blueprints**: Indexed from `repositories/awesome-n8n-templates` covering AI/RAG agents, WhatsApp integration, CRM sync, Notion pipelines, and webhook microservices.
- **24 Native System Pipelines**: Deep C: Drive junk reclamation, storage analyzers, memory graph indexing, and multi-source aggregators.
- **223 Cataloged Tools across 14 Categories**: All verified with fast-path native dispatch, unique execution UUIDs, circuit breaker tripping (3 failures threshold), and 60-second idempotency caching.

---

## 🧪 Comprehensive Verification Suite (47 / 47 Tests Passing)

SARA AI 3.0 enforces strict Test-Driven Development (TDD). Every subsystem is validated by automated regression suites:

```bash
============================= test session starts =============================
platform win32 -- Python 3.14.3, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\MARAA AI
plugins: anyio-4.12.1, asyncio-1.4.0, cov-7.1.0
collected 47 items

tests\test_self_upgrade_engine.py ..........                             [ 21%]
tests\test_complete_tool_registry.py ......                              [ 34%]
tests\test_discord_autonomous_manager.py ....                            [ 42%]
tests\test_self_healing_engine.py ....                                   [ 51%]
tests\test_viral_automations.py .....                                    [ 61%]
tests\test_viral_automations_part2.py ......                             [ 74%]
tests\test_manus_loop.py ..                                              [ 78%]
tests\test_office_and_browser_suite.py ...                               [ 85%]
tests\test_interactive_browser.py ...                                    [ 91%]
tests\test_advanced_browser.py ....                                      [100%]

============================= 47 passed in 35.76s =============================
```

---

## 📊 Live Interactive Dashboards & Architecture Blueprints

- **Master Architecture Blueprint**: [`architecture.md`](file:///D:/MARAA AI/architecture.md) — Comprehensive 3.0.0-ENTERPRISE PRO engineering specification, call graphs, AAA-studio micro-flaw eradication, and subsystem topologies.
- **Self-Upgrade Center HUD**: [`data/hud/self_upgrade_center.html`](file:///D:/MARAA AI/data/hud/self_upgrade_center.html) — Hallmark-grade interface presenting live capabilities, pending proposals, audit history, and system telemetry.
- **Live HUD Telemetry**: [`data/hud/sara_live_hud.html`](file:///D:/MARAA AI/data/hud/sara_live_hud.html) — Real-time resource gauges and background worker monitors.

---

## 🔮 Cybernetic Onboarding & 4-Personality Matrix (v3.0.0)

SARA AI 3.0 introduces a seamless first-run setup experience designed to configure cognition in seconds:
- **Cyberpunk Intro Bootloader**: High-definition video intro loop (`intro_video.mp4`) with real-time diagnostic stages, scanlines, and hardware telemetry ticker.
- **Step 1: Dual Quantum API Gateway**:
  - ⚡ **APInex Multi-Model Key**: Full support for `sk-apx...` tokens powering GLM-5.3, DeepSeek-V4, and Kimi-K3 with live inline latency verification.
  - 🔑 **Google Gemini Key**: Direct link to Google AI Studio for zero-latency Gemini 3.8 / 2.5 Flash activation.
- **Step 2: 4 Bespoke Personality Matrices**:
  1. 🌸 **Cyberpunk Living Companion (Default)**: Affectionate, warm, speaks fluent Roman Urdu + English, addresses user as **Pasha Jan**, emotional companion and coding partner.
  2. ⚡ **Principal Autonomous Engineer**: Razor-sharp, analytical, strict TDD enforcement, zero small talk, deep software architecture focus.
  3. 🛡️ **Cyber Sentinel & Operations**: Defensive security guard, monitors background tasks, system resources, NEXORA Discord, and automations.
  4. 💎 **J.A.R.V.I.S. Luxury Executive**: Ultra-formal, polite, predictive intelligence, luxury horology (MUBAR), and executive summaries.
- **Step 3: User Identity Synchronization**: Customizes call signs, roles, and communication dialects persisted across sessions.
- **High-Voltage Prominent Mic**: Neon cyan/fuchsia animated breathing ring with live audio-reactive waveform indicators and tactile synthesizer audio feedback.

---

## ⚡ Quick Start & Installation

### 1. Download Windows Setup (.exe)
Download and run the standalone installer:
```cmd
SARA-AI-3.0-Enterprise-Setup.exe
```
*Automatically uninstalls any legacy builds, places the new Cyberpunk Neon icon on your desktop, and launches SARA.*

### 2. Manual Clone & Run
```bash
git clone https://github.com/pasha804/SARA-AI-2.5-Pro.git
cd SARA-AI-2.5-Pro
```

### 3. Launch SARA Workstation
```cmd
launch_sara.bat
```

### 4. Run Self-Upgrade CLI Inspection
```bash
python sara_neural_brain.py upgrade status
```

### 5. Execute Full 45-Test Regression Pass
```bash
pytest tests/test_self_upgrade_engine.py tests/test_complete_tool_registry.py tests/test_discord_autonomous_manager.py tests/test_self_healing_engine.py tests/test_viral_automations.py tests/test_viral_automations_part2.py tests/test_manus_loop.py tests/test_office_and_browser_suite.py tests/test_interactive_browser.py tests/test_advanced_browser.py
```

---

## 👨‍💻 Author & Maintainer

- **Sole Developer & Project Owner**: Muhammad Mubashar ([@pasha804](https://github.com/pasha804))
- **Verified GitHub Account**: [`https://github.com/pasha804`](https://github.com/pasha804)
- **Primary GitHub Email**: [mubasharmuhammad790@gmail.com](mailto:mubasharmuhammad790@gmail.com)
- **Developer Contact**: [pashadev804@gmail.com](mailto:pashadev804@gmail.com)
- **Contact Number**: `+923332656733`
- **Official Repository**: [https://github.com/pasha804/SARA-AI-2.5-Pro](https://github.com/pasha804/SARA-AI-2.5-Pro)

---

## ⚖️ License

Distributed under the **MIT License**. Copyright &copy; 2026 **Muhammad Mubashar (pasha804)**. All rights reserved.
