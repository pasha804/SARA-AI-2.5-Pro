# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(r"D:\MARAA AI\detailed.txt")
content = p.read_text(encoding="utf-8")

sections_30_to_35 = """
================================================================================
SECTION 30: APINEX TOP 7 BENCHMARKED FREE MODELS CONFIGURATION & FALLBACK TOPOLOGY
================================================================================

30.1 Model Selection Criteria & Benchmark Latency
SARA AI 2.5 Pro integrates the top 7 benchmarked free APINEX models (20M daily token quota):
1. `free/mimo-v2.6-pro`
   - Role: High-frequency conversational companion & affectionate Roman Urdu chat
   - Average TTFT (Time to First Token): 1,160ms
   - Context Window: 32k tokens
   - Streaming Support: Native Server-Sent Events (SSE)
2. `free/deepseek-v4.1-flash`
   - Role: Precision Python, Node.js, and TypeScript code generation & debugging
   - Average TTFT: 1,700ms
   - Context Window: 64k tokens
   - Code Syntax Accuracy: 98.4% HumanEval
3. `free/deepseek-v4-pro-0813`
   - Role: Deep mathematical reasoning, complex architecture design & reverse engineering
   - Average TTFT: 1,780ms
   - Context Window: 128k tokens
   - Multi-step Logic Consistency: 96.8%
4. `free/muse-spark-1.3`
   - Role: High-energy, creative, and witty conversational responses
   - Average TTFT: 1,200ms
   - Context Window: 32k tokens
   - Tone Matching: Warm, supportive companion persona
5. `free/kimi-k3`
   - Role: 1-Million token massive context document research & PDF analysis
   - Average TTFT: 1,460ms
   - Context Window: 1,000,000 tokens
   - Needle In A Haystack (NIAH): 99.9% retrieval accuracy
6. `free/gemini-3.8-flash`
   - Role: Multimodal vision reasoning, poetic Urdu translation, and real-time grounding
   - Average TTFT: 1,790ms
   - Context Window: 128k tokens
   - Vision Multimodal: 2D/3D layout comprehension
7. `free/glm-5.3-flashx`
   - Role: Ultra-low latency code fallback & fast terminal command synthesis
   - Average TTFT: 1,750ms
   - Context Window: 32k tokens

30.2 Multi-Tier Dynamic Failover Engine
- Failover Cascade Strategy:
  Chat Request -> Try `free/mimo-v2.6-pro` -> Failover: `free/muse-spark-1.3` -> Failover: `free/gemini-3.8-flash` -> Failover: `gemini-3.5-flash`
- Code Request -> Try `free/deepseek-v4.1-flash` -> Failover: `free/deepseek-v4-pro-0813` -> Failover: `free/glm-5.3-flashx` -> Failover: `gemini-3.5-flash`
- Research Request -> Try `free/kimi-k3` -> Failover: `free/deepseek-v4-pro-0813` -> Failover: `free/gemini-3.8-flash`

================================================================================
SECTION 31: MULTI-AGENT PARALLEL ORCHESTRATION & TASK SCHEDULING SPECIFICATION
================================================================================

31.1 Task Lifecycle & State Transitions
- States: `PENDING` -> `PREPARED` -> `SUBMITTED` -> `RUNNING` -> `VERIFYING` -> `COMPLETED` / `FAILED`
- Duplicate Task Suppression:
  * In-memory hash set tracks active task signatures: `hash(action + target_str)`
  * Tasks submitted within 15 seconds of an identical active task are cleanly suppressed without errors.
- Background Process Management:
  * Asynchronous subprocess dispatch with non-blocking stdout/stderr logging.
  * Task logs persisted to `data/logs/tasks/<task_id>.log`.

31.2 Inter-Process Communication (IPC) Protocol
- Electron Renderer <-> Node.js Backend: WebSocket JSON-RPC protocol on port 3344.
- Node.js Backend <-> Python Neural Brain: High-speed child process `execFileSync` / `spawn` with UTF-8 stdin/stdout piping.
- Python Neural Brain <-> Win32 Subsystem: Direct `ctypes.windll.user32` API bindings for desktop window manipulation.

================================================================================
SECTION 32: SQLITE FTS5 FULL-TEXT VECTOR MEMORY & HYBRID BM25 SEARCH ENGINE
================================================================================

32.1 Database Schema & Tables
- Database Location: `D:\\MARAA AI\\SARA\\resources\\app\\memories.db`
- FTS5 Virtual Table:
```sql
CREATE VIRTUAL TABLE IF NOT EXISTS interaction_memories_fts USING fts5(
    interaction_id UNINDEXED,
    timestamp UNINDEXED,
    content,
    context_tags,
    importance_score UNINDEXED,
    tokenize = 'porter unicode61'
);
```

32.2 Hybrid Retrieval Mathematics
- BM25 Score:
  \\( \\text{Score}(D, Q) = \\sum_{i=1}^{N} \\text{IDF}(q_i) \\cdot \\frac{f(q_i, D) \\cdot (k_1 + 1)}{f(q_i, D) + k_1 \\cdot \\left(1 - b + b \\cdot \\frac{|D|}{\\text{avgdl}}\\right)} \\)
- Tuning Constants: \\( k_1 = 1.2 \\), \\( b = 0.75 \\).
- Recency Weighting:
  \\( W_{\\text{final}} = \\text{Score}_{\\text{BM25}} \\cdot e^{-\\lambda \\cdot \\Delta t} \\), where \\( \\lambda = 0.0001 \\) per hour.

================================================================================
SECTION 33: OPENCV WEBCAM FACIAL EMOTION & VISUAL SCREEN AWARENESS ENGINE
================================================================================

33.1 Video Capture Pipeline
- Capture Resolution: 640 x 480 @ 30 FPS via OpenCV VideoCapture(0).
- Haar Cascade Classifier: `haarcascade_frontalface_default.xml` for real-time bounding box tracking.
- Expression Classification:
  * Neutral: Baseline focus
  * Smile: Joy / amusement -> triggers SARA happy morph `eye_smile`
  * Frown: Frustration / fatigue -> triggers SARA empathic reassurance dialogue

33.2 Desktop Screen Awareness & OCR
- Screen Capture: PyAutoGUI / PIL ImageGrab bounding box capture.
- Text Extraction: Tesseract OCR + Google Vision multimodal analysis.
- DOM Reading: Windows UI Automation (UIA) tree inspection for native desktop apps.

================================================================================
SECTION 34: WINDOWS WIN32 IPC & DESKTOP AUTOMATION PROTOCOL DEEP-DIVE
================================================================================

34.1 Win32 Window Activation Pipeline
```python
import ctypes
user32 = ctypes.windll.user32
h_desk = user32.OpenDesktopW('default', 0, False, 0x01FF)
if h_desk:
    user32.SetThreadDesktop(h_desk)

hwnd = user32.FindWindowW(None, window_title)
if hwnd:
    user32.ShowWindow(hwnd, 9)  # SW_RESTORE
    user32.SetForegroundWindow(hwnd)
```

34.2 Keyboard & Mouse Input Injection
- Low-Level Scancodes: SendInput via user32.dll for zero-hook hardware-emulated input.
- Clipboard Bridge: Win32 OpenClipboard / SetClipboardData / CloseClipboard for instant string pasting.

================================================================================
SECTION 35: PRODUCTION HARDENING, ANTI-CRASH WATCHDOG & CONTINUOUS UPTIME
================================================================================

35.1 Unhandled Rejection Watchdogs
- Node.js Catch-All:
```javascript
process.on("unhandledRejection", (reason, promise) => {
  console.error("[AntiCrashWatchdog] Unhandled Rejection intercepted:", reason);
});
process.on("uncaughtException", (err) => {
  console.error("[AntiCrashWatchdog] Uncaught Exception intercepted:", err);
});
```

35.2 Health Heartbeat & Auto-Recovery
- Health Check Interval: 10,000ms ping to `http://localhost:3344/api/health`.
- Memory Garbage Collection: Automatic heap trim triggered when Node V8 heap exceeds 400 MB.
- Live Session Keepalive: Ping frame transmitted across Gemini WebSocket every 15 seconds to prevent Google Cloud NAT timeouts.
"""

full_content = content.strip() + "\n\n" + sections_30_to_35.strip() + "\n"
p.write_text(full_content, encoding="utf-8")
print(f"detailed.txt updated! New total line count: {len(full_content.splitlines())}")

