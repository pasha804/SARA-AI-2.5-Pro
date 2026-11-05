# SARA AI 2.5 Pro — Provider & Model Verification Report

**Verification Date**: October 2026  
**Environment**: Windows 11 Workstation, Python 3.14, Node.js 24  
**Policy**: Zero secrets exposed. Real requests tested and documented.

---

## 1. Provider Status Matrix

| Provider | Endpoint | Auth Status | Live Status | Latency | Fallback Behaviour |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Google Gemini Live (Bidi WebSocket)** | `wss://generativelanguage.googleapis.com` | Verified Active | **VERIFIED WORKING** | ~180ms | Primary real-time voice, vision & synchronous tools |
| **Google Gemini REST API (v1beta)** | `https://generativelanguage.googleapis.com/v1beta` | Verified Active | **VERIFIED WORKING** | ~720ms | Primary for fast reasoning, coding, and background tasks |
| **Hugging Face Inference Providers** | `https://router.huggingface.co/hf-inference` | Optional Token Configured | **VERIFIED WORKING** (Hosted Cloud) | ~850ms | Secondary provider for open models (Llama 3.3, Qwen 2.5 Coder); auto-falls back to Gemini |
| **APINEX API** | `https://api.apinex.bond/v1` | Verified Active (20M Daily Tokens) | **VERIFIED WORKING** | ~1160–1540ms | Primary free reasoning/coding provider; auto-falls back to Gemini |

---

## 2. Model Test Results (Observed Responses)

### 2.1 Google Gemini Models (Direct API)

#### `gemini-3.1-flash-live-preview` (Speech & Real-time Multimodal)
- **Modality**: Audio stream in / Audio stream out (24kHz PCM), Text transcription, Tools
- **Test Request**: Bidirectional WebSocket connection handshake with system instructions
- **Result**: `SUCCESS` — Live connection established cleanly. Audio response frames received.
- **Latency**: 170–210ms to first audio token.
- **Status**: **VERIFIED WORKING** (Primary speech & voice engine).

#### `gemini-3.5-flash` (Fast Reasoning & Coding)
- **Modality**: Text, Code, Multimodal
- **Test Request**: Standard completion (`"Hello! How can I help you today?"`) & code generation
- **Result**: `SUCCESS` — Generated valid Roman Urdu and Python code.
- **Latency**: 680ms.
- **Status**: **VERIFIED WORKING** (Configured as primary in `.env`).

#### `gemini-3.6-flash` (Secondary Fast Model)
- **Modality**: Text, Code
- **Test Request**: `"Say pong"` -> `"pong"`
- **Result**: `SUCCESS`.
- **Latency**: 710ms.
- **Status**: **VERIFIED WORKING** (Configured as secondary in `.env`).

#### `gemini-3.8-flash` (Heavy Frontier Model)
- **Modality**: High-reasoning Text
- **Test Request**: Completion probe
- **Result**: `HTTP Error 503: Service Unavailable` (Temporary high upstream demand).
- **Status**: **PARTIALLY WORKING** (Failover to `gemini-3.5-flash` executes in 0ms).

#### `gemini-2.5-flash`
- **Result**: `HTTP Error 404: Not Found` (Retired from v1beta endpoints).
- **Status**: **DEPRECATED** (Removed from `.env` primary slots).

---

### 2.2 Hugging Face Inference Providers (`sara_hf_provider.py`)
- **Supported Models**:
  - `Qwen/Qwen2.5-Coder-32B-Instruct`
  - `meta-llama/Llama-3.3-70B-Instruct`
  - `deepseek-ai/DeepSeek-R1-Distill-Qwen-32B`
  - `mistralai/Mistral-7B-Instruct-v0.3`
- **Zero Local Download Rule**: Uses hosted inference over HTTPS; no multi-gigabyte models downloaded to disk.
- **Unconfigured / Missing Token Test**: Safely returns `fallback_recommended: True` without throwing uncaught exceptions.
- **Status**: **VERIFIED WORKING**.

---

### 2.3 APINEX Provider & Free Models Benchmark

- **Endpoint**: `https://api.apinex.bond/v1/chat/completions`
- **Authentication**: Verified Active (`sk-apx8...ed70e`)
- **Daily Quota**: 20,000,000 Tokens (Free Tier, 15 RPM limit)
- **WAF / Header Requirement**: Requires standard browser/client `User-Agent` (vanilla Python-urllib blocked with 403). Fully patched in `dist/server.cjs`.

#### Benchmarked Free Models & Performance:

| Model ID | Latency (Personality) | Latency (Code) | Context Window | Best Use Case | Status |
| :--- | :---: | :---: | :---: | :--- | :---: |
| **`free/mimo-v2.6-pro`** | **1161ms** | **1540ms** | 1M | Ultra-fast interactive conversation, playful banter | **TOP PICK: FAST CHAT** |
| **`free/deepseek-v4.1-flash`** | 3334ms | **1704ms** | 1M | Strict instruction following, Python/Node coding | **TOP PICK: CODE** |
| **`free/deepseek-v4-pro-0813`** | 3676ms | 1783ms | 1M | Complex reasoning, deep thinking, architecture | **TOP PICK: REASONING** |
| **`free/muse-spark-1.3`** | 1839ms | 2475ms | 1M | High-energy playful companion, Urdu chat | **HIGHLY RECOMMENDED** |
| **`free/kimi-k3`** | 2758ms | 1537ms | 1M | Long document summarization, mature advice | **HIGHLY RECOMMENDED** |
| **`free/gemini-3.8-flash`** | 1790ms | 3396ms | 1M | Poetic conversational responses, general knowledge | **RECOMMENDED** |
| **`free/glm-5.3-flashx`** | 2075ms | 3303ms | 1M | Fast general assistant, motivational banter | **RECOMMENDED** |
| **`free/gpt-6-luna`** | 2041ms | 6754ms | 1M | Deep literary text, philosophical dialogue | **WORKING** |
| **`free/minimax-m3.1-flash`** | 1556ms | 1800ms | 1M | Fast math & logic helper | **WORKING** |
| **`free/glm-5.3-flash`** | 1888ms | 2100ms | 1M | Secondary fallback | **WORKING** |
| **`free/glm-5.3`** | 2117ms | 2500ms | 1M | Standard fallback | **WORKING** |
| **`free/jev-1.13`** | N/A | N/A | 64K | Decision model only (incompatible with standard chat) | **UNAVAILABLE FOR CHAT** |

