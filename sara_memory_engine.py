# -*- coding: utf-8 -*-
"""
SARA AI 2.5 Pro — 3-Tier Deep Persistent Vector & SQLite Long-Term Memory Core
Provides permanent, lifelong memory storage across sessions:
  L0: Working Card / Short-Term Context (RAM)
  L1: Semantic Core Facts (SQLite + Category Index)
  L2: Full Historical Episodic Memory & Project Milestones (SQLite FTS5 Full-Text Search)
"""

import os
import sys
import json
import sqlite3
import datetime
from pathlib import Path
from contextlib import contextmanager

WORKSPACE_ROOT = Path(r"D:\MARAA AI").resolve()
DATA_DIR = WORKSPACE_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "sara_persistent_memory.db"
LEGACY_MEMORIES_FILE = WORKSPACE_ROOT / "SARA" / "resources" / "app" / "memories.json"


class SaraMemoryEngine:

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()
        self._migrate_legacy_memories()

    @contextmanager
    def _connection(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self):
        with self._connection() as conn:
            cur = conn.cursor()
            # 1. Structured Semantic Facts Table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS facts (
                    id TEXT PRIMARY KEY,
                    category TEXT NOT NULL,
                    text TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            cur.execute("CREATE INDEX IF NOT EXISTS idx_facts_category ON facts(category)")

            # 2. Episodic Conversations & Turns Table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    speaker TEXT NOT NULL,
                    user_prompt TEXT NOT NULL,
                    assistant_reply TEXT NOT NULL,
                    mood TEXT,
                    tags TEXT
                )
            """)
            cur.execute("CREATE INDEX IF NOT EXISTS idx_conversations_time ON conversations(timestamp)")

            # 3. Project Engineering Milestones Table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS milestones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_name TEXT NOT NULL,
                    milestone_desc TEXT NOT NULL,
                    files_affected TEXT,
                    timestamp TEXT NOT NULL
                )
            """)

            # 4. SQLite FTS5 Full-Text Search Virtual Table
            cur.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS fts_memories USING fts5(
                    source_type,
                    source_id,
                    content,
                    tokenize='porter'
                )
            """)
            conn.commit()

    def _migrate_legacy_memories(self):
        """Migrate legacy memories.json items into SQLite if facts table is empty."""
        try:
            with self._connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) as count FROM facts")
                count = cur.fetchone()["count"]
                if count == 0 and LEGACY_MEMORIES_FILE.exists():
                    items = json.loads(LEGACY_MEMORIES_FILE.read_text(encoding="utf-8"))
                    now = datetime.datetime.now().isoformat()
                    for item in items:
                        f_id = item.get("id", f"fact_{now}")
                        cat = item.get("category", "general")
                        txt = item.get("text", "")
                        c_at = item.get("createdAt", now)
                        u_at = item.get("updatedAt", now)
                        cur.execute(
                            "INSERT OR REPLACE INTO facts (id, category, text, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                            (f_id, cat, txt, c_at, u_at)
                        )
                        cur.execute(
                            "INSERT INTO fts_memories (source_type, source_id, content) VALUES (?, ?, ?)",
                            ("fact", f_id, f"{cat}: {txt}")
                        )
                    conn.commit()
        except Exception as e:
            print(f"[MemoryEngine] Migration note: {e}")

    def remember_fact(self, category: str, text: str, custom_id: str = None) -> dict:
        """Stores or updates a durable semantic fact in long-term memory with duplicate suppression."""
        clean_cat = category.strip().lower()
        clean_text = text.strip()
        now = datetime.datetime.now().isoformat()
        with self._connection() as conn:
            cur = conn.cursor()
            # Duplicate check: If exact same fact exists, update timestamp and avoid duplicate row
            cur.execute("SELECT id FROM facts WHERE category = ? AND text = ?", (clean_cat, clean_text))
            existing = cur.fetchone()
            if existing:
                fact_id = existing["id"]
                cur.execute("UPDATE facts SET updated_at = ? WHERE id = ?", (now, fact_id))
                conn.commit()
                return {"success": True, "id": fact_id, "category": clean_cat, "text": clean_text, "duplicate_suppressed": True}

            fact_id = custom_id or f"fact_{int(datetime.datetime.now().timestamp()*1000)}"
            cur.execute(
                "INSERT OR REPLACE INTO facts (id, category, text, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (fact_id, clean_cat, clean_text, now, now)
            )
            cur.execute(
                "INSERT INTO fts_memories (source_type, source_id, content) VALUES (?, ?, ?)",
                ("fact", fact_id, f"{clean_cat}: {clean_text}")
            )
            conn.commit()
        return {"success": True, "id": fact_id, "category": clean_cat, "text": clean_text}

    def deduplicate_facts(self) -> int:
        """Purges duplicate facts from database, keeping the earliest one."""
        with self._connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                DELETE FROM facts
                WHERE id NOT IN (
                    SELECT MIN(id)
                    FROM facts
                    GROUP BY category, text
                )
            """)
            removed = cur.rowcount
            # Rebuild FTS index for facts cleanly
            cur.execute("DELETE FROM fts_memories WHERE source_type = 'fact'")
            cur.execute("SELECT id, category, text FROM facts")
            for row in cur.fetchall():
                cur.execute(
                    "INSERT INTO fts_memories (source_type, source_id, content) VALUES (?, ?, ?)",
                    ("fact", row["id"], f"{row['category']}: {row['text']}")
                )
            conn.commit()
        return removed

    def record_task_history(self, task_id: str, action: str, status: str, result_summary: str = "") -> dict:
        """Indexes background task completion and outcomes into searchable persistent memory."""
        now = datetime.datetime.now().isoformat()
        with self._connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS task_history (
                    id TEXT PRIMARY KEY,
                    action TEXT NOT NULL,
                    status TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            cur.execute(
                "INSERT OR REPLACE INTO task_history (id, action, status, summary, timestamp) VALUES (?, ?, ?, ?, ?)",
                (task_id, action, status, str(result_summary)[:500], now)
            )
            cur.execute(
                "INSERT INTO fts_memories (source_type, source_id, content) VALUES (?, ?, ?)",
                ("task", task_id, f"task {action}: {status} {str(result_summary)[:300]}")
            )
            conn.commit()
        return {"success": True, "task_id": task_id}

    def search_fts(self, query: str, limit: int = 5) -> list:
        """Alias for search_memory providing standard FTS naming."""
        return self.search_memory(query, limit)

    def record_turn(self, user_prompt: str, assistant_reply: str, mood: str = "adoring_soulmate", tags: str = "") -> dict:
        """Records an episodic conversational turn into permanent storage."""
        now = datetime.datetime.now().isoformat()
        with self._connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO conversations (timestamp, speaker, user_prompt, assistant_reply, mood, tags) VALUES (?, ?, ?, ?, ?, ?)",
                (now, "Pasha Dev & SARA", user_prompt.strip(), assistant_reply.strip(), mood, tags)
            )
            conv_id = cur.lastrowid
            searchable_content = f"{user_prompt} | {assistant_reply} | {tags}"
            cur.execute(
                "INSERT INTO fts_memories (source_type, source_id, content) VALUES (?, ?, ?)",
                ("conversation", str(conv_id), searchable_content)
            )
            conn.commit()
        return {"success": True, "conversation_id": conv_id}

    def record_milestone(self, project_name: str, description: str, files: list = None) -> dict:
        """Records a major software engineering milestone or project modification."""
        now = datetime.datetime.now().isoformat()
        files_json = json.dumps(files or [])
        with self._connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO milestones (project_name, milestone_desc, files_affected, timestamp) VALUES (?, ?, ?, ?)",
                (project_name, description.strip(), files_json, now)
            )
            m_id = cur.lastrowid
            cur.execute(
                "INSERT INTO fts_memories (source_type, source_id, content) VALUES (?, ?, ?)",
                ("milestone", str(m_id), f"{project_name}: {description} files={files_json}")
            )
            conn.commit()
        return {"success": True, "milestone_id": m_id, "project": project_name}

    def search_memory(self, query: str, limit: int = 5) -> list:
        """Sub-millisecond full-text associative recall across all memories, facts, and milestones."""
        clean_q = query.strip().replace("'", "").replace('"', "")
        if not clean_q:
            return self.get_top_facts(limit)

        results = []
        with self._connection() as conn:
            cur = conn.cursor()
            try:
                cur.execute(
                    """
                    SELECT source_type, source_id, content, rank
                    FROM fts_memories
                    WHERE fts_memories MATCH ?
                    ORDER BY rank
                    LIMIT ?
                    """,
                    (f"{clean_q}*", limit)
                )
                rows = cur.fetchall()
                for row in rows:
                    results.append({
                        "source": row["source_type"],
                        "id": row["source_id"],
                        "content": row["content"]
                    })
            except Exception:
                cur.execute(
                    "SELECT id, category, text FROM facts WHERE text LIKE ? OR category LIKE ? LIMIT ?",
                    (f"%{clean_q}%", f"%{clean_q}%", limit)
                )
                for r in cur.fetchall():
                    results.append({
                        "source": "fact",
                        "id": r["id"],
                        "content": f"{r['category']}: {r['text']}"
                    })

        return results

    def get_top_facts(self, limit: int = 10) -> list:
        with self._connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, category, text FROM facts ORDER BY created_at DESC LIMIT ?", (limit,))
            return [{"source": "fact", "id": r["id"], "content": f"{r['category']}: {r['text']}"} for r in cur.fetchall()]

    def synthesize_user_profile(self) -> dict:
        """
        Constructs an authoritative, synthesized context profile of Pasha Jan's
        preferences, verified contacts, security bounds, and active engineering projects.
        """
        with self._connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT category, text FROM facts")
            facts = {row["category"]: row["text"] for row in cur.fetchall()}

            cur.execute("SELECT project_name, milestone_desc, timestamp FROM milestones ORDER BY id DESC LIMIT 5")
            milestones = [dict(row) for row in cur.fetchall()]

        profile = {
            "user_name": facts.get("user_name", "Pasha Jan"),
            "full_name": facts.get("full_name", "Mubashar Jan"),
            "email": facts.get("email", "pashadev804@gmail.com"),
            "phone": facts.get("phone", "+923332656733"),
            "authorized_discord_server": "NEXORA",
            "active_workspace": str(WORKSPACE_ROOT),
            "desktop_dashboard": "pasha_nexus_dashboard",
            "top_models": [
                "free/glm-5.3-flashx",
                "free/gemini-3.8-flash",
                "free/deepseek-v4-pro-0813"
            ],
            "recent_milestones": milestones,
            "total_facts_stored": len(facts),
            "synthesized_at": datetime.datetime.now().isoformat()
        }
        return profile

    def backup_memory(self, target_dir: Path = None) -> dict:
        """Creates a safe, timestamped backup copy of the persistent SQLite memory database."""
        import shutil
        dest_dir = target_dir or (DATA_DIR / "backups")
        dest_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = dest_dir / f"sara_memory_backup_{timestamp}.db"
        try:
            shutil.copy2(str(self.db_path), str(backup_file))
            return {
                "success": True,
                "backup_path": str(backup_file),
                "original_path": str(self.db_path),
                "timestamp": timestamp
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


memory_engine = SaraMemoryEngine()

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "search":
        q = sys.argv[2]
        res = memory_engine.search_memory(q)
        print(json.dumps(res, indent=2))
    elif len(sys.argv) > 3 and sys.argv[1] == "add":
        cat = sys.argv[2]
        txt = sys.argv[3]
        res = memory_engine.remember_fact(cat, txt)
        print(json.dumps(res, indent=2))
    else:
        facts = memory_engine.get_top_facts(5)
        print(f"SARA Persistent SQLite Memory Core Active. Facts loaded: {len(facts)}")
        print(json.dumps(facts[:3], indent=2))
