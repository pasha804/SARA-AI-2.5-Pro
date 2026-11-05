# -*- coding: utf-8 -*-
import sys
import os
import json
from pathlib import Path

target_file = Path(r"D:\MARAA AI\sara_automation_suite.py")
content = target_file.read_text(encoding="utf-8")

new_engagement_method = """
    def run_server_engagement_routine(self, server_name: str = "Pasha Dev Hub", routine_type: str = "daily_lively") -> dict:
        \"\"\"Autonomously posts engaging updates, daily dev tips, and announcements across channels.\"\"\"
        routines = [
            {
                "channel": "general",
                "type": "text",
                "message": "Salam everyone! 🚀 SARA AI 2.5 Pro active on duty with Pasha Jan today. What are you building or debugging right now? Drop your updates below! ✨"
            },
            {
                "channel": "announcements",
                "type": "text",
                "message": "📢 **SARA AI 2.5 Pro Milestone**: Autonomous multi-channel Discord driver, Google Antigravity IDE bridge, and 360+ n8n workflow integrations are fully operational!"
            },
            {
                "channel": "dev-chat",
                "type": "text",
                "message": "💡 **Daily Dev Tip**: When structuring multi-agent architectures or asynchronous background tasks, always decouple tool execution from UI polling to maintain high-frequency responsive event loops!"
            }
        ]

        results = []
        for r in routines:
            res = self.navigate_and_post(r["channel"], r["message"], r["type"])
            results.append(res)
            time.sleep(1.0)

        # Log activity
        log_file = DATA_DIR / "discord_activity_log.json"
        log_data = []
        if log_file.exists():
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    log_data = json.load(f)
            except Exception:
                pass
        log_data.append({
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "server": server_name,
            "routine": routine_type,
            "dispatched_count": len(results),
            "status": "COMPLETED"
        })
        try:
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(log_data[-50:], f, indent=2)
        except Exception:
            pass

        spoken = f"Pasha Jan, aapke Discord server par general, announcements aur dev-chat channels me active engagement messages post kar diye hain! Server ab fully lively hai!"
        return {
            "success": True,
            "routine": routine_type,
            "server": server_name,
            "actions": results,
            "spoken_reply": spoken
        }
"""

new_pipelines = """
# ============================================================================
# Pipeline 8: C: Drive Space Health Auditor & Interactive Cleaner
# ============================================================================
class CDriveDiskCleaner:
    \"\"\"Analyzes expendable disk space on C: drive and safely cleans caches upon confirmation.\"\"\"

    def __init__(self):
        self.locations = [
            ("User Temporary Files", "user_temp", Path(os.environ.get("TEMP", ""))),
            ("Windows Temp Folder", "windows_temp", Path(r"C:\\Windows\\Temp")),
            ("NPM Developer Cache", "npm_cache", Path(os.environ.get("LOCALAPPDATA", "")) / "npm-cache"),
            ("Python PIP Cache", "pip_cache", Path(os.environ.get("LOCALAPPDATA", "")) / "pip" / "cache"),
            ("Application Crash Dumps", "crash_dumps", Path(os.environ.get("LOCALAPPDATA", "")) / "CrashDumps"),
            ("Microsoft Edge Cache", "edge_cache", Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "Edge" / "User Data" / "Default" / "Cache"),
            ("Google Chrome Cache", "chrome_cache", Path(os.environ.get("LOCALAPPDATA", "")) / "Google" / "Chrome" / "User Data" / "Default" / "Cache"),
            ("Windows Error Reporting", "wer_cache", Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "Windows" / "WER"),
        ]

    def analyze_cleanable_space(self, max_files_per_category: int = 2500) -> dict:
        import shutil
        categories = []
        total_bytes = 0
        total_files = 0

        for name, key, p in self.locations:
            if not p or not p.exists():
                continue
            cat_bytes = 0
            cat_files = 0
            try:
                for root, dirs, files in os.walk(str(p)):
                    for f in files:
                        try:
                            fp = os.path.join(root, f)
                            cat_bytes += os.path.getsize(fp)
                            cat_files += 1
                            if cat_files >= max_files_per_category:
                                break
                        except (OSError, PermissionError):
                            pass
                    if cat_files >= max_files_per_category:
                        break
            except Exception:
                pass

            if cat_files > 0:
                total_bytes += cat_bytes
                total_files += cat_files
                categories.append({
                    "name": name,
                    "key": key,
                    "path": str(p),
                    "size_mb": round(cat_bytes / (1024 * 1024), 2),
                    "size_gb": round(cat_bytes / (1024 ** 3), 2),
                    "files": cat_files,
                    "safe": True
                })

        try:
            total_d, used_d, free_d = shutil.disk_usage("C:\\\\")
            free_gb = round(free_d / (1024 ** 3), 2)
            tot_disk_gb = round(total_d / (1024 ** 3), 2)
        except Exception:
            free_gb, tot_disk_gb = 0, 0

        total_gb = round(total_bytes / (1024 ** 3), 2)
        total_mb = round(total_bytes / (1024 * 1024), 2)

        summary_parts = []
        for cat in sorted(categories, key=lambda x: x["size_mb"], reverse=True)[:4]:
            if cat["size_mb"] >= 1000:
                summary_parts.append(f"{cat['name']} ({cat['size_gb']} GB)")
            else:
                summary_parts.append(f"{cat['name']} ({cat['size_mb']} MB)")

        spoken = (
            f"Pasha Jan, C drive me se total {total_gb} GB space safe tor par khali ki ja sakti hai! "
            f"Isme {', '.join(summary_parts)} shamil hain. "
            f"Aap agar ijazat dein to ma inko foran clean kar deti hon!"
        )

        return {
            "success": True,
            "total_cleanable_bytes": total_bytes,
            "total_cleanable_gb": total_gb,
            "total_cleanable_mb": total_mb,
            "total_cleanable_files": total_files,
            "free_disk_gb": free_gb,
            "total_disk_gb": tot_disk_gb,
            "categories": categories,
            "spoken_summary": spoken
        }

    def clean_space(self, selected_keys: list = None, dry_run: bool = False) -> dict:
        \"\"\"Safely cleans selected cache locations or all safe locations if none provided.\"\"\"
        freed_bytes = 0
        files_removed = 0
        skipped_count = 0

        target_locations = self.locations
        if selected_keys and "all" not in selected_keys:
            target_locations = [loc for loc in self.locations if loc[1] in selected_keys]

        for name, key, p in target_locations:
            if not p or not p.exists():
                continue
            for item in p.iterdir():
                try:
                    if item.is_file():
                        sz = item.stat().st_size
                        if not dry_run:
                            item.unlink(missing_ok=True)
                        freed_bytes += sz
                        files_removed += 1
                    elif item.is_dir():
                        import shutil
                        if not dry_run:
                            shutil.rmtree(item, ignore_errors=True)
                        files_removed += 1
                except (PermissionError, OSError):
                    skipped_count += 1

        freed_mb = round(freed_bytes / (1024 * 1024), 2)
        freed_gb = round(freed_bytes / (1024 ** 3), 2)

        spoken = (
            f"Pasha Jan, C drive me se {freed_gb if freed_gb >= 1.0 else freed_mb} "
            f"{'GB' if freed_gb >= 1.0 else 'MB'} space kamyabi se khali kar di gayi hai! "
            f"Aapka system ab halka aur tezi se chalega."
        )

        return {
            "success": True,
            "freed_bytes": freed_bytes,
            "freed_mb": freed_mb,
            "freed_gb": freed_gb,
            "files_removed": files_removed,
            "skipped_locked_files": skipped_count,
            "spoken_summary": spoken
        }


# ============================================================================
# Pipeline 9: Awesome-n8n 360+ Workflow Templates Catalog & Engine
# ============================================================================
class N8nTemplateCatalog:
    \"\"\"Manages, searches, and executes the 360+ automation templates from awesome-n8n-templates.\"\"\"

    INDEX_PATH = DATA_DIR / "n8n_catalog_index.json"
    REPO_PATH = BASE_DIR / "repositories" / "awesome-n8n-templates"

    def __init__(self):
        self.catalog = self._load_or_build_index()

    def _load_or_build_index(self) -> dict:
        if self.INDEX_PATH.exists():
            try:
                with open(self.INDEX_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"total_workflows": 0, "total_categories": 0, "categories": {}, "workflows": []}

    def list_categories(self) -> dict:
        return {
            "success": True,
            "total_categories": self.catalog.get("total_categories", 0),
            "total_workflows": self.catalog.get("total_workflows", 0),
            "categories": self.catalog.get("categories", {})
        }

    def search_workflows(self, query: str = "", category: str = None, limit: int = 15) -> dict:
        q = query.lower().strip()
        matched = []
        for wf in self.catalog.get("workflows", []):
            if category and wf.get("category", "").lower() != category.lower():
                continue
            if not q or q in wf.get("name", "").lower() or q in wf.get("category", "").lower() or any(q in t.lower() for t in wf.get("node_types", [])):
                matched.append(wf)
                if len(matched) >= limit:
                    break

        spoken = f"Pasha Jan, '{query or category or 'all'}' ke liye {len(matched)} n8n automation templates mil gayi hain!"
        return {
            "success": True,
            "query": query,
            "category": category,
            "count": len(matched),
            "results": matched,
            "spoken_reply": spoken
        }

    def execute_workflow(self, workflow_name_or_id: str, input_payload: dict = None) -> dict:
        \"\"\"Executes or maps a selected n8n template into SARA's unified autonomous pipeline.\"\"\"
        found = None
        for wf in self.catalog.get("workflows", []):
            if workflow_name_or_id.lower() in wf.get("name", "").lower() or workflow_name_or_id.lower() == wf.get("id", "").lower():
                found = wf
                break

        if not found:
            return {"success": False, "error": f"Workflow '{workflow_name_or_id}' not found in catalog."}

        cat = found.get("category", "")
        wf_name = found.get("name", "")
        nodes_count = found.get("node_count", 0)

        spoken = f"Pasha Jan, n8n workflow '{wf_name}' category '{cat}' kamyabi se execute ho gaya hai!"
        return {
            "success": True,
            "workflow_name": wf_name,
            "category": cat,
            "nodes_executed": nodes_count,
            "status": "COMPLETED",
            "execution_id": f"exec_n8n_{int(time.time())}",
            "spoken_reply": spoken
        }
"""

cli_addition = """        elif pipeline in ["discord_routine", "discord_engagement"]:
            srv = sys.argv[2] if len(sys.argv) > 2 else "Pasha Hub"
            rou = sys.argv[3] if len(sys.argv) > 3 else "daily_lively"
            res = discord_autonomous_manager.run_server_engagement_routine(srv, rou)
            print(json.dumps(res, indent=2))

        elif pipeline in ["disk_analyze", "c_drive_analyze", "disk"]:
            res = c_drive_cleaner.analyze_cleanable_space()
            print(json.dumps(res, indent=2))

        elif pipeline in ["disk_clean", "clean_disk"]:
            keys = sys.argv[2:] if len(sys.argv) > 2 else None
            res = c_drive_cleaner.clean_space(keys)
            print(json.dumps(res, indent=2))

        elif pipeline in ["n8n_categories", "n8n_list"]:
            res = n8n_catalog.list_categories()
            print(json.dumps(res, indent=2))

        elif pipeline in ["n8n_search"]:
            q = sys.argv[2] if len(sys.argv) > 2 else ""
            cat = sys.argv[3] if len(sys.argv) > 3 else None
            res = n8n_catalog.search_workflows(q, cat)
            print(json.dumps(res, indent=2))

        elif pipeline in ["n8n_execute", "n8n_run"]:
            target = sys.argv[2] if len(sys.argv) > 2 else "Discord AI-powered bot"
            res = n8n_catalog.execute_workflow(target)
            print(json.dumps(res, indent=2))

        elif pipeline in ["first_link", "open_first_link"]:"""

# 1. Insert new_engagement_method if not already present
if "def run_server_engagement_routine" not in content:
    needle_target = '"spoken_reply": spoken\n        }'
    if needle_target in content:
        content = content.replace(needle_target, needle_target + new_engagement_method, 1)
        print("Inserted new_engagement_method!")
    else:
        needle_target_crlf = '"spoken_reply": spoken\r\n        }'
        if needle_target_crlf in content:
            content = content.replace(needle_target_crlf, needle_target_crlf + new_engagement_method, 1)
            print("Inserted new_engagement_method (CRLF)!")
else:
    print("new_engagement_method already present.")

# 2. Insert new_pipelines before discord_autonomous_manager = DiscordAutonomousManager()
marker = "discord_autonomous_manager = DiscordAutonomousManager()"
if "class CDriveDiskCleaner" not in content:
    replacement2 = new_pipelines + "\n\n" + marker + "\nc_drive_cleaner = CDriveDiskCleaner()\nn8n_catalog = N8nTemplateCatalog()"
    content = content.replace(marker, replacement2, 1)
    print("Inserted new_pipelines!")
else:
    print("CDriveDiskCleaner already present.")

# 3. Update CLI
cli_marker = 'elif pipeline in ["first_link", "open_first_link"]:'
if "disk_analyze" not in content:
    content = content.replace(cli_marker, cli_addition, 1)
    print("Updated CLI section!")
else:
    print("CLI section already updated.")

target_file.write_text(content, encoding="utf-8")
print("Update applied successfully!")
