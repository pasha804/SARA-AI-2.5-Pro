# SARA AI 2.5 Pro — 3-Tier Deep Persistent Memory Architecture

**Module**: `SARA/resources/app/sara_memory_engine.py`  
**Database**: `D:\MARAA AI\data\sara_persistent_memory.db` (SQLite + FTS5)  
**Short-Term Context**: `AppData\Roaming\sara\working_context.json`  
**Dialogue Storage**: `AppData\Roaming\sara\dialogue_history.json`

---

## 1. Multi-Tier Memory Pyramid

```
┌────────────────────────────────────────────────────────┐
│ L0: Active Working Context (RAM & working_context.json) │
│ - Current active task, active project, recent actions   │
├────────────────────────────────────────────────────────┤
│ L1: Semantic Structured Core Facts (SQLite `facts`)     │
│ - Category-indexed facts (creator, preferences, style)  │
│ - Exact updates & deletions, zero amnesia across boots  │
├────────────────────────────────────────────────────────┤
│ L2: Historical Episodic Memory (SQLite FTS5)            │
│ - Full-text search across dialogue turns & projects     │
│ - Fast snippet matching & relevance scoring             │
└────────────────────────────────────────────────────────┘
```

---

## 2. Zero-Amnesia Dialogue Continuity (`dialogue_history.json`)

To prevent conversation context loss during runtime reconnects or restarts:
1. `globalDialogueHistory` in `server.cjs` is persisted to disk on every turn.
2. When the Gemini Live session refreshes or reconnects, up to **20 complete turns** are restored with `[ACTIVE ONGOING CONVERSATION CONTEXT - ZERO AMNESIA CONTINUITY]`.
3. Speech transcription is consolidated to eliminate interim speech fragments.
4. Response buffers are flushed immediately on interruption to prevent previous responses from bleeding into new conversations.

---

## 3. Database Schema

### Table: `facts`
- `id` (TEXT PRIMARY KEY)
- `category` (TEXT NOT NULL, indexed)
- `text` (TEXT NOT NULL)
- `created_at` (TEXT ISO8601)
- `updated_at` (TEXT ISO8601)

### Table: `conversations`
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `session_id` (TEXT)
- `role` (TEXT: `user` or `sara`)
- `content` (TEXT)
- `timestamp` (TEXT)

### Virtual Table: `conversations_fts`
- Using `fts5(content, role, session_id)` for sub-millisecond keyword and context retrieval.

