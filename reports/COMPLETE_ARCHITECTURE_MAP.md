# SARA AI 2.5 — COMPLETE ARCHITECTURE MAP
**Project**: SARA AI 2.5.0 ENTERPRISE PRO  
**Owner & Principal**: Muhammad Mubashar (Pasha Dev) (`pashadev804@gmail.com`, `+923332656733`)  
**Audit Date**: November 8, 2026  
**Knowledge Graph Source**: `graphify-out/graph.json` (1,984 Nodes, 3,485 Edges, 186 Communities)  
**Root Path**: `D:\MARAA AI`  

---

## 1. System High-Level Topology

```mermaid
graph TB
    subgraph Client ["Desktop Client Tier"]
        UI["Electron 32 Frontend (port 3344)"]
        ThreeCanvas["Three.js 0.180 WebGL Viewport"]
        LiveHUD["JARVIS Holographic HUD Canvas"]
        AudioIn["Microphone 24kHz PCM Capture"]
        AudioOut["AudioContext 24kHz Playback & FFT"]
    end

    subgraph Server ["Gateway Tier (Node.js)"]
        ServerCJS["server.cjs (Process Coordinator)"]
        WSGateway["WebSocket Gateway (:3344)"]
        GeminiClient["Gemini Live 3.8 Bidirectional Stream"]
        ScreenObserver["desktopCapturer (1440p Screen Capture)"]
        FastDispatcher["executeNodeNativeTool() (222 Unified Tools)"]
    end

    subgraph CoreEngine ["Cognitive Tier (Python Brain)"]
        NeuralBrain["sara_neural_brain.py (CLI Gateway)"]
        CognitiveRuntime["CognitiveRuntime & AutonomousMind"]
        MemoryEngine["sara_memory_engine.py & ClaudeMem"]
        TaskManager["sara_task_manager.py (PST Scheduler)"]
        AntigravityBridge["sara_antigravity_bridge.py (IDE RPC)"]
    end

    subgraph ExecutionEngines ["Autonomous Execution Tier"]
        BrowserEngine["sara_interactive_browser.py (Playwright Chromium)"]
        DiscordEngine["DiscordAutonomousManager (NEXORA Guild)"]
        ManusLoop["sara_manus_loop.py (Planning with Files)"]
        OfficeEngine["sara_office_and_browser_suite.py (Word/PPT)"]
        ViralAutomations["sara_advanced_viral_automations.py (32 Repos)"]
        SelfHealing["sara_self_healing_engine.py (Self-Repair)"]
    end

    UI --> WSGateway
    WSGateway <--> GeminiClient
    GeminiClient -->|toolCall| FastDispatcher
    FastDispatcher -->|Direct Node FS/Exec| ServerCJS
    FastDispatcher -->|CLI Process Invocation| NeuralBrain
    NeuralBrain --> CognitiveRuntime
    CognitiveRuntime --> MemoryEngine
    CognitiveRuntime --> TaskManager
    CognitiveRuntime --> AntigravityBridge
    NeuralBrain --> BrowserEngine
    NeuralBrain --> DiscordEngine
    NeuralBrain --> ManusLoop
    NeuralBrain --> OfficeEngine
    NeuralBrain --> ViralAutomations
    NeuralBrain --> SelfHealing
```

---

## 2. Component Directory & File References

| Layer | Primary Source Files | Function & Responsibility |
|---|---|---|
| **Frontend UI** | [index.html](file:///D:/MARAA%20AI/SARA/resources/app/dist/index.html) | Electron canvas hosting 3D VRM avatar, HUD overlays, Web Audio FFT lip-sync. |
| **Gateway** | [server.cjs](file:///D:/MARAA%20AI/SARA/resources/app/dist/server.cjs) | WebSocket RPC server, Gemini Live connection, fast-path tool dispatcher. |
| **Neural Brain** | [sara_neural_brain.py](file:///D:/MARAA%20AI/sara_neural_brain.py) | Cognitive execution hub, multi-agent personality, CLI subcommands. |
| **Browser Agent** | [sara_interactive_browser.py](file:///D:/MARAA%20AI/sara_interactive_browser.py) | Playwright Chromium automation, DOM element inspection, smart field fill, PyAutoGUI fallback. |
| **Discord Intelligence** | [sara_automation_suite.py](file:///D:/MARAA%20AI/sara_automation_suite.py#L380-L550) | NEXORA Discord community manager, channel routing, rate-limit protection. |
| **Manus Loop** | [sara_manus_loop.py](file:///D:/MARAA%20AI/sara_manus_loop.py) | Autonomous multi-step goal execution with state machine persistence. |
| **Office Suite** | [sara_office_and_browser_suite.py](file:///D:/MARAA%20AI/sara_office_and_browser_suite.py) | Automated `.docx` authoring and `.pptx` presentation generation. |
| **Viral Repos Suite** | [sara_advanced_viral_automations.py](file:///D:/MARAA%20AI/sara_advanced_viral_automations.py) | Repomix, Firecrawl, Vibe-Kanban, Headroom token guard, Caveman compressor. |
| **Viral Repos Part 2**| [sara_viral_automations_part2.py](file:///D:/MARAA%20AI/sara_viral_automations_part2.py) | Claude-Mem, Beads DAG pipeline, Model Router, Taste-Skill linter, Live HUD, CC-Switch. |
| **Memory Engine** | [sara_memory_engine.py](file:///D:/MARAA%20AI/sara_memory_engine.py) | Episodic and associative vector persistence, conversation continuity. |
| **Task Manager** | [sara_task_manager.py](file:///D:/MARAA%20AI/sara_task_manager.py) | PST timezone-aware cron scheduling, background worker loops. |
| **Path Resolver** | [sara_path_resolver.py](file:///D:/MARAA%20AI/sara_path_resolver.py) | Strict path canonicalization, Windows path jailing, safety validation. |
| **Self Healing** | [sara_self_healing_engine.py](file:///D:/MARAA%20AI/sara_self_healing_engine.py) | Automated root-cause isolation, AST patch generation, verified regression checks. |

---

## 3. Data Flow Architectures

### 3.1 Multimodal Voice & Audio Stream Flow
1. User speaks into microphone -> Electron AudioWorklet captures 24kHz PCM 16-bit mono.
2. PCM chunks stream via WebSocket to `server.cjs` -> forwarded to Gemini Live 3.8.
3. Gemini Live returns 24kHz PCM audio chunks -> `server.cjs` streams to Electron client.
4. Electron Web Audio `AnalyserNode` computes FFT bins:
   - 300Hz–1200Hz -> `Fcl_MTH_A` / `Fcl_MTH_O` (open jaw).
   - 1200Hz–3500Hz -> `Fcl_MTH_I` / `Fcl_MTH_E` (wide teeth/smile).
   - Pauses (<0.02 amplitude) -> Smooth exponential release to closed lips.

### 3.2 Multimodal Screen Perception Flow
1. Gemini requests screen context or periodic 3-second heartbeat activates.
2. `server.cjs` invokes `desktopCapturer.getSources({ types: ['screen'], thumbnailSize: { width: 1440, height: 900 } })`.
3. Electron captures primary display bitmap -> converts to high-compression JPEG buffer.
4. JPEG buffer transmitted as realtime image input to Gemini Live session.

### 3.3 Tool Execution & Reliability Flow
```mermaid
sequenceDiagram
    participant User as User / Gemini Live
    participant Server as server.cjs (Gateway)
    participant Reliability as sara_reliability_engine.py
    participant Subsystem as Target Subsystem (Browser/Discord/Office)

    User->>Server: toolCall(functionName, args)
    Server->>Reliability: execute_with_reliability(tool, args)
    Note over Reliability: Verify schema, generate UUID, check idempotency cache
    alt Cache Hit (Idempotent)
        Reliability-->>Server: Cached result
    else Cache Miss
        Reliability->>Subsystem: Invoke with timeout & circuit breaker
        alt Subsystem Success
            Subsystem-->>Reliability: Execution result
            Reliability-->>Server: Structured JSON {ok: true, result, telemetry}
        else Subsystem Failure
            Note over Reliability: Trigger exponential backoff retry (if safe)
            alt Retry succeeds
                Subsystem-->>Reliability: Execution result
                Reliability-->>Server: Structured JSON {ok: true, result, retries: 1}
            else Circuit Breaker Open
                Reliability-->>Server: Structured JSON {ok: false, error, classification}
            end
        end
    end
    Server-->>User: safeSendToolResponse(toolName, callId, response)
```

---

## 4. Graphify Knowledge Graph Insights (God Nodes & Clustering)

According to the AST dependency analysis in `graphify-out/graph.json`:
- **Total Entities Mapped**: 1,984 Nodes, 3,485 Edges, 186 Communities.
- **Import Cycles**: 0 (Clean Directed Acyclic Graph across core modules).
- **Identified God Nodes**:
  1. `TestAll120ToolsLive` (Degree: 42) — Central automated testing harness.
  2. `record_tool_audit()` (Degree: 38) — Test auditing and verification registry.
  3. `startServer()` in `server.cjs` (Degree: 34) — Central Node gateway entry point.
  4. `CognitiveRuntime` in `sara_neural_brain.py` (Degree: 28) — Multi-agent dispatch.
  5. `SaraInteractiveBrowserAgent` in `sara_interactive_browser.py` (Degree: 24) — Browser automation.
  6. `DiscordAutonomousManager` in `sara_automation_suite.py` (Degree: 22) — Discord controller.

---

## 5. Security & Safety Guardrails

1. **Discord Guild Hard Lock**:
   - `DiscordAutonomousManager` contains strict assertion checks requiring `guild.id == "1430932596956270634"` (`NEXORA`). Any action targeting external servers throws an immediate `SecurityViolationError`.
2. **Path Sanitization & Jailing**:
   - All filesystem operations are filtered through `sara_path_resolver.py` to prevent directory traversal outside `D:\MARAA AI`, `Desktop`, and `Downloads`.
3. **Destructive Action Confirmation**:
   - Operations that delete files, format drives, or terminate non-automation processes require explicit confirmation envelopes or are rejected outright.
4. **Secret Masking**:
   - Passwords, API tokens, and Discord keys are redacted using regex filters before appearing in logs or HUD telemetry.

---
*Certified by Principal Systems Architect & Senior Security Engineer.*

