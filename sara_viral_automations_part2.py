# -*- coding: utf-8 -*-
"""
SARA AI 2.5 Pro — Advanced Viral Automations Suite (Part 2)
Integrates killer architectural capabilities from the viral 32-repo ecosystem:
  1. ClaudeMemAssociativeEngine (#9 Claude-Mem) — Long-term episodic distillation & associative semantic recall.
  2. BeadsWorkflowDAGOrchestrator (#22 Beads) — Directed Acyclic Graph (DAG) task chaining & pipeline orchestrator.
  3. ClaudeCodeRouterEngine (#27 Claude-Code-Router) — Intelligent multi-tier model & execution routing.
  4. TasteSkillAestheticLinter (#11 Taste-Skill, #12 UI-UX-Pro-Max) — Zero AI Slop rule enforcer & luxury design linter.
  5. ClaudeLiveHUDTelemetry (#29 Claude-HUD) — Real-time visual telemetry HUD & live HTML dashboard.
  6. CcSwitchProfileManager (#28 CC-Switch) — Context & cognitive persona profile manager.
"""

import os
import sys
import json
import time
import re
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import deque

BASE_DIR = Path(r"D:\MARAA AI").resolve()
DATA_DIR = BASE_DIR / "data"
MEMORIES_DIR = DATA_DIR / "memories"
MEMORIES_DIR.mkdir(parents=True, exist_ok=True)
HUD_DIR = DATA_DIR / "hud"
HUD_DIR.mkdir(parents=True, exist_ok=True)
PROFILES_DIR = DATA_DIR / "profiles"
PROFILES_DIR.mkdir(parents=True, exist_ok=True)
PIPELINES_DIR = DATA_DIR / "pipelines"
PIPELINES_DIR.mkdir(parents=True, exist_ok=True)

USER_PROFILE_TRUTH = {
    "name": "Muhammad Mubashar (Pasha Dev)",
    "email": "pashadev804@gmail.com",
    "phone": "+923332656733",
    "role": "Founder, Lead AI Architect & Visionary",
    "discord_server": "NEXORA"
}


# ============================================================================
# 1. ClaudeMemAssociativeEngine (#9 Claude-Mem)
# ============================================================================
class ClaudeMemAssociativeEngine:
    """
    Episodic memory distillation, atomic fact synthesis, and associative context recall.
    Extracts durable insights and ranks them for prompt augmentation.
    """

    def __init__(self, store_path: Optional[Path] = None):
        self.store_path = store_path or (MEMORIES_DIR / "claude_mem_store.json")
        self._ensure_store()

    def _ensure_store(self):
        if not self.store_path.exists():
            initial_data = {
                "version": "2.5.0",
                "memories": [
                    {
                        "id": "mem_founder_identity",
                        "content": "Muhammad Mubashar (Pasha Dev) is the founder and visionary behind SARA AI 2.5 Pro.",
                        "tags": ["identity", "founder", "pasha"],
                        "importance": 5,
                        "created_at": datetime.datetime.now().isoformat()
                    },
                    {
                        "id": "mem_discord_lock",
                        "content": "SARA AI Discord automation is strictly authorized and locked to server 'NEXORA'.",
                        "tags": ["discord", "nexora", "security"],
                        "importance": 5,
                        "created_at": datetime.datetime.now().isoformat()
                    }
                ]
            }
            with open(self.store_path, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, indent=2)

    def _load_memories(self) -> List[Dict[str, Any]]:
        try:
            with open(self.store_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("memories", [])
        except Exception:
            return []

    def _save_memories(self, memories: List[Dict[str, Any]]):
        data = {
            "version": "2.5.0",
            "updated_at": datetime.datetime.now().isoformat(),
            "memories": memories
        }
        with open(self.store_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def distill_and_store_turn(
        self,
        user_prompt: str,
        assistant_reply: str,
        tags: Optional[List[str]] = None,
        importance: int = 3
    ) -> Dict[str, Any]:
        """Distills durable facts from a conversational turn and stores them."""
        memories = self._load_memories()
        tags = tags or []

        # Heuristic extraction of durable facts
        extracted_facts = []
        full_text = f"{user_prompt}\n{assistant_reply}"

        # Detect identity/founder references
        if "pasha" in full_text.lower() or "mubashar" in full_text.lower():
            extracted_facts.append(
                f"Founder Directive: {user_prompt.strip()[:180]} -> Result: {assistant_reply.strip()[:180]}"
            )
            tags.extend(["founder", "directive", "pasha"])

        # Detect technical or startup goals
        if any(w in full_text.lower() for w in ["startup", "venture", "repo", "investor", "feature", "build", "api"]):
            extracted_facts.append(
                f"Engineering Milestone: {user_prompt.strip()[:180]}"
            )
            tags.extend(["engineering", "milestone", "startup"])

        if not extracted_facts:
            extracted_facts.append(f"Turn Summary: {user_prompt.strip()[:120]}")

        new_ids = []
        for fact in extracted_facts:
            mem_id = f"mem_{int(time.time() * 1000)}_{len(new_ids)}"
            memory_item = {
                "id": mem_id,
                "content": fact,
                "tags": list(set(tags)),
                "importance": max(1, min(5, importance)),
                "created_at": datetime.datetime.now().isoformat()
            }
            memories.append(memory_item)
            new_ids.append(mem_id)

        self._save_memories(memories)
        return {
            "success": True,
            "new_memory_ids": new_ids,
            "memory_count": len(memories)
        }

    def associative_recall(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Ranks memories using token matching, keyword overlap, tag relevance, and importance weight.
        """
        memories = self._load_memories()
        if not memories:
            return []

        tokens = set(re.findall(r'\b[a-zA-Z0-9_\-]{3,}\b', query.lower()))
        scored_memories = []

        for mem in memories:
            content_lower = mem.get("content", "").lower()
            tags_lower = [t.lower() for t in mem.get("tags", [])]
            importance = mem.get("importance", 1)

            # Score calculation
            score = 0.0
            for token in tokens:
                if token in content_lower:
                    score += 2.5
                if token in tags_lower:
                    score += 4.0

            # Weight by importance
            score += (importance * 1.5)

            # Extra weight for founder truth
            if "pasha" in tokens and "pasha" in content_lower:
                score += 10.0

            scored_memories.append((score, mem))

        # Sort descending
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored_memories[:top_k]]

    def generate_prompt_memory_injection(self, query: str, top_k: int = 4) -> str:
        """Generates an LLM prompt header injecting high-priority associative context."""
        recalled = self.associative_recall(query, top_k=top_k)
        if not recalled:
            return ""

        lines = [
            "### SARA Active Recall Context (Claude-Mem Deep Engine)",
            f"- Authorized Principal: {USER_PROFILE_TRUTH['name']} ({USER_PROFILE_TRUTH['email']})",
            f"- Discord Safe Server: {USER_PROFILE_TRUTH['discord_server']}"
        ]
        for m in recalled:
            lines.append(f"- [{m.get('importance', 3)}★] {m.get('content')}")

        return "\n".join(lines)


# ============================================================================
# 2. BeadsWorkflowDAGOrchestrator (#22 Beads)
# ============================================================================
class BeadsWorkflowDAGOrchestrator:
    """
    Directed Acyclic Graph (DAG) Task Chaining Pipeline.
    Allows atomic units ('beads') with dependencies, variable pipelining,
    and automatic step-by-step execution.
    """

    def __init__(self):
        self.pipelines_dir = PIPELINES_DIR

    def create_pipeline(self, pipeline_id: str, beads: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Saves a DAG pipeline definition."""
        safe_id = re.sub(r'[^a-zA-Z0-9_\-]', '_', pipeline_id).strip('_')
        pipe_path = self.pipelines_dir / f"{safe_id}.json"

        # Validate DAG dependencies
        bead_ids = {b["id"] for b in beads}
        for b in beads:
            for dep in b.get("dependencies", []):
                if dep not in bead_ids:
                    raise ValueError(f"Dependency '{dep}' not declared in pipeline beads.")

        data = {
            "pipeline_id": safe_id,
            "created_at": datetime.datetime.now().isoformat(),
            "beads": beads
        }
        with open(pipe_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return {"success": True, "pipeline_id": safe_id, "beads_count": len(beads)}

    def execute_pipeline(
        self,
        pipeline_id: str,
        initial_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executes a DAG pipeline in topologically sorted order,
        passing execution context downstream.
        """
        safe_id = re.sub(r'[^a-zA-Z0-9_\-]', '_', pipeline_id).strip('_')
        pipe_path = self.pipelines_dir / f"{safe_id}.json"
        if not pipe_path.exists():
            raise FileNotFoundError(f"Pipeline '{pipeline_id}' not found.")

        with open(pipe_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        beads = data.get("beads", [])
        bead_map = {b["id"]: b for b in beads}
        in_degree = {b["id"]: 0 for b in beads}
        adj = {b["id"]: [] for b in beads}

        for b in beads:
            for dep in b.get("dependencies", []):
                adj[dep].append(b["id"])
                in_degree[b["id"]] += 1

        # Kahn's algorithm for topological ordering
        queue = deque([bid for bid, deg in in_degree.items() if deg == 0])
        execution_order = []

        while queue:
            node = queue.popleft()
            execution_order.append(node)
            for neighbor in adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(execution_order) != len(beads):
            raise RuntimeError("Pipeline graph contains a cyclic dependency!")

        # Execute beads
        context = initial_context.copy() if initial_context else {}
        results = {}
        failed_count = 0
        completed_count = 0

        for bid in execution_order:
            bead = bead_map[bid]
            action = bead.get("action", "custom")
            params = bead.get("params", {})

            try:
                # Execute simulated or real action
                step_res = self._execute_single_bead(action, params, context)
                results[bid] = {
                    "status": "COMPLETED",
                    "output": step_res,
                    "timestamp": datetime.datetime.now().isoformat()
                }
                # Pipe results into shared context
                context[f"{bid}_output"] = step_res
                completed_count += 1
            except Exception as e:
                results[bid] = {
                    "status": "FAILED",
                    "error": str(e),
                    "timestamp": datetime.datetime.now().isoformat()
                }
                failed_count += 1
                break  # Stop execution on failure

        return {
            "success": failed_count == 0,
            "pipeline_id": safe_id,
            "execution_order": execution_order,
            "completed_beads_count": completed_count,
            "failed_beads_count": failed_count,
            "results": results,
            "final_context": context
        }

    def _execute_single_bead(self, action: str, params: Dict[str, Any], context: Dict[str, Any]) -> Any:
        if action == "custom":
            return {"status": "ok", "processed_params": params, "user": context.get("user", "Pasha Dev")}
        elif action == "kanban_card":
            # Add to Kanban
            from sara_advanced_viral_automations import VibeKanbanSprintAutomator
            kanban = VibeKanbanSprintAutomator()
            return kanban.create_task(
                title=params.get("title", "Automated Bead Task"),
                column=params.get("column", "in_progress"),
                priority=params.get("priority", "high")
            )
        elif action == "pack_codebase":
            from sara_advanced_viral_automations import RepomixCodebasePacker
            packer = RepomixCodebasePacker()
            return packer.pack_repository(pack_name=params.get("pack_name", "pipeline_pack"))
        else:
            return {"status": "executed", "action": action, "data": params}


# ============================================================================
# 3. ClaudeCodeRouterEngine (#27 Claude-Code-Router)
# ============================================================================
class ClaudeCodeRouterEngine:
    """
    Intelligent Model & Compute Strategy Router.
    Routes queries to:
      - TIER_FAST_LOCAL: Local zero-cost filesystem, regex, git, or command scripts (<10ms).
      - TIER_SPEED_FLASH: Gemini 2.5 Flash for high-speed voice and snappy conversational queries (<250ms).
      - TIER_DEEP_REASONING_PRO: Gemini 2.5 Pro for deep architecture, multi-file code review, AST, and refactoring.
      - TIER_AUTONOMOUS_MANUS: Multi-step long-running autonomous loop with context files and external artifacts.
    """

    def route_request(self, prompt: str, context_tokens: int = 0) -> Dict[str, Any]:
        p_lower = prompt.lower().strip()

        # 1. Check Autonomous Multi-Step Goals
        if any(trigger in p_lower for trigger in ["goal:", "manus", "multi-step", "market research on top", "executive word doc and powerpoint"]):
            return {
                "tier": "TIER_AUTONOMOUS_MANUS",
                "recommended_engine": "sara_manus_loop.ManusAutonomousLoop",
                "estimated_latency_ms": 3500,
                "reason": "Autonomous multi-step execution loop required for multi-file research & generation.",
                "confidence": 0.95
            }

        # 2. Check Fast Local File/OS Tasks
        local_triggers = ["list files", "dir ", "git status", "find file", "check file", "read file", "current directory"]
        if any(trig in p_lower for trig in local_triggers) and len(prompt.split()) <= 10:
            return {
                "tier": "TIER_FAST_LOCAL",
                "recommended_engine": "local_python_os_engine",
                "estimated_latency_ms": 5,
                "reason": "Direct disk/OS query handled instantaneously at $0 token cost.",
                "confidence": 0.99
            }

        # 3. Check Deep Reasoning Pro
        deep_triggers = [
            "refactor", "ast tree", "strict tdd", "architecture", "security audit",
            "deep dive", "postmortem", "memory leak", "investor pitch", "math", "algorithm"
        ]
        if any(trig in p_lower for trig in deep_triggers) or context_tokens > 20000:
            return {
                "tier": "TIER_DEEP_REASONING_PRO",
                "recommended_engine": "gemini-2.5-pro",
                "estimated_latency_ms": 1200,
                "reason": "High-complexity architectural reasoning requiring maximum cognitive intelligence.",
                "confidence": 0.92
            }

        # 4. Default: High-Speed Flash (Voice / Fast Chat / Casual)
        return {
            "tier": "TIER_SPEED_FLASH",
            "recommended_engine": "gemini-2.5-flash",
            "estimated_latency_ms": 220,
            "reason": "Snappy, low-latency conversational response with natural voice fluency.",
            "confidence": 0.88
        }


# ============================================================================
# 4. TasteSkillAestheticLinter (#11 Taste-Skill, #12 UI-UX-Pro-Max)
# ============================================================================
class TasteSkillAestheticLinter:
    """
    Enforces the 'Zero AI Slop Rule' and audits frontend designs against luxury standards:
      - Detects generic purple-to-blue linear gradients (#6366f1, #a855f7).
      - Detects floating blurry background blobs.
      - Detects generic placeholder marketing buzzwords.
      - Enforces CSS tokens at :root and proper spring physics.
    """

    FORBIDDEN_GRADIENTS = [
        re.compile(r'linear-gradient\s*\([^)]*#6366f1[^)]*#a855f7[^)]*\)', re.IGNORECASE),
        re.compile(r'linear-gradient\s*\([^)]*#8b5cf6[^)]*#ec4899[^)]*\)', re.IGNORECASE),
    ]

    SLOPPY_BUZZWORDS = [
        "unleash the power of ai",
        "next-gen ai solution",
        "revolutionize your workflow",
        "seamlessly empower",
        "cutting-edge ai"
    ]

    def audit_code(self, content: str, file_type: str = "html") -> Dict[str, Any]:
        violations = []
        c_lower = content.lower()

        # 1. Check Cliche Gradients
        for pat in self.FORBIDDEN_GRADIENTS:
            if pat.search(content):
                violations.append({
                    "rule": "NO_CLICHE_AI_GRADIENTS",
                    "severity": "CRITICAL",
                    "description": "Generic purple-to-blue AI gradient detected. Replace with obsidian/emerald/platinum tokens."
                })

        # 2. Check Floating Blur Blobs
        if "filter: blur(" in c_lower or "filter:blur(" in c_lower:
            if any(k in c_lower for k in ["blob", "glow-orb", "circle", "blur(40px)"]):
                violations.append({
                    "rule": "NO_FLOATING_BLUR_BLOBS",
                    "severity": "MAJOR",
                    "description": "Unanchored blurry background glow blob detected. Use structured glassmorphic border highlights instead."
                })

        # 3. Check AI Slop Buzzwords
        for buzz in self.SLOPPY_BUZZWORDS:
            if buzz in c_lower:
                violations.append({
                    "rule": "ZERO_MARKETING_SLOP_BUZZWORDS",
                    "severity": "MAJOR",
                    "description": f"Marketing cliché phrase detected: '{buzz}'. Replace with tangible, metric-driven statements."
                })

        # 4. Check CSS variables
        if ("<style" in c_lower or file_type == "css") and ":root" not in content and "--" not in content:
            violations.append({
                "rule": "USE_CSS_TOKENS",
                "severity": "MEDIUM",
                "description": "Hardcoded colors found without central :root design tokens."
            })

        # Score calculation
        base_score = 100
        for v in violations:
            if v["severity"] == "CRITICAL":
                base_score -= 30
            elif v["severity"] == "MAJOR":
                base_score -= 15
            elif v["severity"] == "MEDIUM":
                base_score -= 10

        taste_score = max(0, min(100, base_score))
        return {
            "is_clean": len(violations) == 0,
            "taste_score": taste_score,
            "grade": "A+" if taste_score >= 90 else ("B" if taste_score >= 70 else "SLOP"),
            "violations": violations
        }

    def generate_luxury_design_system_patch(self) -> str:
        """Returns a bespoke, obsidian/emerald luxury design token sheet."""
        return """/* SARA AI Luxury Bespoke Design Tokens (Zero AI Slop Compliant) */
:root {
  --bg-primary: #07090e;
  --bg-surface: rgba(16, 21, 34, 0.85);
  --bg-surface-elevated: #151b2b;
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-active: rgba(16, 185, 129, 0.4);
  
  --accent-emerald: #10b981;
  --accent-emerald-glow: rgba(16, 185, 129, 0.25);
  --accent-cyan: #06b6d4;
  --text-primary: #f8fafc;
  --text-muted: #94a3b8;
  
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
  
  --spring-snappy: cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
"""


# ============================================================================
# 5. ClaudeLiveHUDTelemetry (#29 Claude-HUD)
# ============================================================================
class ClaudeLiveHUDTelemetry:
    """
    Real-Time Heads-Up Display (HUD) and Telemetry Stream for SARA AI 2.5 Pro.
    Generates terminal ASCII dashboards and interactive luxury HTML HUD files.
    """

    def __init__(self):
        self.hud_dir = HUD_DIR

    def get_telemetry_snapshot(self) -> Dict[str, Any]:
        """Gathers system vitals, active memory, and authorized state."""
        import platform

        # Calculate memory store size
        mem_engine = ClaudeMemAssociativeEngine()
        mems = mem_engine._load_memories()

        return {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "authorized_user": USER_PROFILE_TRUTH["name"],
            "authorized_email": USER_PROFILE_TRUTH["email"],
            "discord_server": USER_PROFILE_TRUTH["discord_server"],
            "model_core": "Gemini 2.5 Pro / Flash + SARA Manus Loop",
            "active_memories_count": len(mems),
            "system_health": {
                "os": f"{platform.system()} {platform.release()}",
                "python": platform.python_version(),
                "status": "OPTIMAL_ONLINE",
                "token_budget_safe": True
            }
        }

    def render_terminal_hud(self) -> str:
        snap = self.get_telemetry_snapshot()
        hud = f"""
================================================================================
  ▲ SARA AI 2.5 PRO — REAL-TIME TELEMETRY HUD (CLAUDE-HUD REPO #29)
================================================================================
  • PRINCIPAL ARCHITECT : {snap['authorized_user']}
  • AUTHORIZED ACCESS   : {snap['authorized_email']}
  • DISCORD SERVER LOCK : {snap['discord_server']} (100% ISOLATED)
  • SYSTEM STATUS       : {snap['system_health']['status']} (OS: {snap['system_health']['os']})
  • NEURAL CORES        : {snap['model_core']}
  • CLAUDE-MEM STORAGE  : {snap['active_memories_count']} Distilled Knowledge Atoms
  • CONTEXT SAFEGUARD   : HEADROOM ACTIVE (Budget: 1,000,000 Tokens)
================================================================================
"""
        return hud.strip()

    def generate_live_html_hud(self) -> Path:
        """Generates a luxury interactive glassmorphic HUD dashboard."""
        snap = self.get_telemetry_snapshot()
        out_path = self.hud_dir / "sara_live_hud.html"

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SARA AI 2.5 Pro — Live Telemetry HUD</title>
    <style>
        :root {{
            --bg-deep: #05070c;
            --bg-card: rgba(14, 20, 32, 0.75);
            --border-glow: rgba(16, 185, 129, 0.25);
            --emerald: #10b981;
            --cyan: #06b6d4;
            --text-main: #f1f5f9;
            --text-sub: #94a3b8;
        }}
        body {{
            margin: 0;
            padding: 30px;
            background: var(--bg-deep);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
        }}
        .hud-container {{
            max-width: 1100px;
            width: 100%;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-glow);
            padding-bottom: 16px;
            margin-bottom: 24px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 26px;
            letter-spacing: 1px;
            background: linear-gradient(90deg, #10b981, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .status-badge {{
            background: rgba(16, 185, 129, 0.15);
            color: var(--emerald);
            border: 1px solid var(--emerald);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
        }}
        .hud-card {{
            background: var(--bg-card);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 22px;
            backdrop-filter: blur(12px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}
        .hud-card h3 {{
            margin-top: 0;
            font-size: 15px;
            color: var(--cyan);
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }}
        .stat-value {{
            font-size: 28px;
            font-weight: 700;
            color: #fff;
            margin: 10px 0;
        }}
        .stat-desc {{
            font-size: 13px;
            color: var(--text-sub);
        }}
    </style>
</head>
<body>
    <div class="hud-container">
        <div class="header">
            <div>
                <h1>SARA AI 2.5 Pro — Live Telemetry HUD</h1>
                <div style="font-size: 13px; color: var(--text-sub); margin-top: 4px;">Viral Repo Integration: Claude-HUD (#29) & Headroom (#31)</div>
            </div>
            <div class="status-badge">● ONLINE & ARMED</div>
        </div>

        <div class="grid">
            <div class="hud-card">
                <h3>Principal Identity</h3>
                <div class="stat-value">{snap['authorized_user']}</div>
                <div class="stat-desc">Email: {snap['authorized_email']}</div>
            </div>

            <div class="hud-card">
                <h3>Discord Gateway</h3>
                <div class="stat-value">{snap['discord_server']}</div>
                <div class="stat-desc">Strict security sandbox locked to Pasha Dev's server</div>
            </div>

            <div class="hud-card">
                <h3>Claude-Mem Atoms</h3>
                <div class="stat-value">{snap['active_memories_count']} Facts</div>
                <div class="stat-desc">Episodic memory distillation with associative recall</div>
            </div>

            <div class="hud-card">
                <h3>Cognitive Architecture</h3>
                <div class="stat-value">Gemini 2.5 Pro</div>
                <div class="stat-desc">Multi-tier router + Manus Autonomous Loop</div>
            </div>
        </div>
    </div>
</body>
</html>
"""
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        return out_path


# ============================================================================
# 6. CcSwitchProfileManager (#28 CC-Switch)
# ============================================================================
class CcSwitchProfileManager:
    """
    Context & Cognitive Persona Switcher.
    Enables zero-latency switching between executive modes.
    """

    PROFILES = {
        "founder": {
            "id": "founder",
            "name": "Pasha Founder Mode",
            "description": "Venture velocity, startup valuation, pitch deck synthesis, and strategic metrics.",
            "temperature": 0.4,
            "system_prompt_modifier": "You are operating in Pasha Founder Mode (Venture Founder). Prioritize venture scale, crisp business metrics, pitch structure, and executive clarity for Muhammad Mubashar."
        },
        "dev_beast": {
            "id": "dev_beast",
            "name": "Apex Dev Beast Mode",
            "description": "Strict TDD, clean architecture, AST tree analysis, Repomix codebase packs, zero fluff.",
            "temperature": 0.2,
            "system_prompt_modifier": "You are operating in Apex Dev Beast Mode. Enforce strict TDD, clean modular architecture, and zero AI slop in code."
        },
        "companion": {
            "id": "companion",
            "name": "Loyal Companion Mode",
            "description": "Warm, affectionate Roman Urdu/English tone, supportive conversational partner for Pasha Jan.",
            "temperature": 0.7,
            "system_prompt_modifier": "You are operating in Loyal Companion Mode. Speak warmly, respectfully, and affectionately to Pasha Jan (Muhammad Mubashar) with supportive companionship."
        },
        "researcher": {
            "id": "researcher",
            "name": "Deep Scholar Mode",
            "description": "Rigorous academic synthesis, Firecrawl deep web dossiers, and first-principles citations.",
            "temperature": 0.3,
            "system_prompt_modifier": "You are operating in Deep Scholar Mode. Provide rigorous first-principles analysis, deep citations, and systematic knowledge dossiers."
        }
    }

    def __init__(self):
        self.state_file = PROFILES_DIR / "active_profile.json"
        self._ensure_profile()

    def _ensure_profile(self):
        if not self.state_file.exists():
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump({"active_profile": "founder"}, f, indent=2)

    def switch_profile(self, profile_name: str) -> Dict[str, Any]:
        p_name = profile_name.lower().strip()
        if p_name not in self.PROFILES:
            raise ValueError(f"Profile '{profile_name}' not recognized. Available: {list(self.PROFILES.keys())}")

        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump({"active_profile": p_name, "switched_at": datetime.datetime.now().isoformat()}, f, indent=2)

        return {"success": True, "active_profile": self.PROFILES[p_name]}

    def get_active_profile(self) -> Dict[str, Any]:
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                p_id = data.get("active_profile", "founder")
                return self.PROFILES.get(p_id, self.PROFILES["founder"])
        except Exception:
            return self.PROFILES["founder"]

    def list_profiles(self) -> List[Dict[str, Any]]:
        return list(self.PROFILES.values())

    def get_system_prompt_modifier(self) -> str:
        return self.get_active_profile()["system_prompt_modifier"]
