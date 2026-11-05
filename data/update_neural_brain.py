# -*- coding: utf-8 -*-
import sys
from pathlib import Path

p = Path(r"D:\MARAA AI\sara_neural_brain.py")
content = p.read_text(encoding="utf-8")

cli_additions = '''        elif cmd == "discord_routine" or cmd == "discord_engagement":
            try:
                from sara_automation_suite import discord_autonomous_manager
                srv = sys.argv[2] if len(sys.argv) > 2 else "Pasha Dev Hub"
                rou = sys.argv[3] if len(sys.argv) > 3 else "daily_lively"
                res = discord_autonomous_manager.run_server_engagement_routine(srv, rou)
                print(json.dumps(res, indent=2))
            except Exception as e:
                print(json.dumps({"success": False, "error": str(e)}))
        elif cmd == "disk_analyze" or cmd == "c_drive_analyze" or cmd == "disk":
            try:
                from sara_automation_suite import c_drive_cleaner
                res = c_drive_cleaner.analyze_cleanable_space()
                print(json.dumps(res, indent=2))
            except Exception as e:
                print(json.dumps({"success": False, "error": str(e)}))
        elif cmd == "disk_clean" or cmd == "clean_disk":
            try:
                from sara_automation_suite import c_drive_cleaner
                keys = sys.argv[2:] if len(sys.argv) > 2 else None
                res = c_drive_cleaner.clean_space(keys)
                print(json.dumps(res, indent=2))
            except Exception as e:
                print(json.dumps({"success": False, "error": str(e)}))
        elif cmd == "n8n_search" or cmd == "search_automations":
            try:
                from sara_automation_suite import n8n_catalog
                q = sys.argv[2] if len(sys.argv) > 2 else ""
                cat = sys.argv[3] if len(sys.argv) > 3 else None
                res = n8n_catalog.search_workflows(q, cat)
                print(json.dumps(res, indent=2))
            except Exception as e:
                print(json.dumps({"success": False, "error": str(e)}))
        elif cmd == "n8n_execute" or cmd == "execute_automation":
            try:
                from sara_automation_suite import n8n_catalog
                target = sys.argv[2] if len(sys.argv) > 2 else "Discord AI-powered bot"
                res = n8n_catalog.execute_workflow(target)
                print(json.dumps(res, indent=2))
            except Exception as e:
                print(json.dumps({"success": False, "error": str(e)}))
        elif cmd == "build_project" or cmd == "create_project":
            try:
                from sara_project_manager import project_manager
                name = sys.argv[2] if len(sys.argv) > 2 else "pasha_nexus_dashboard"
                p_type = sys.argv[3] if len(sys.argv) > 3 else "Full-Stack SaaS Platform"
                res = project_manager.create_autonomous_project(name, p_type)
                print(json.dumps(res, indent=2))
            except Exception as e:
                print(json.dumps({"success": False, "error": str(e)}))
        elif cmd == "self_update" or cmd == "evolve":
            try:
                from sara_self_improvement import self_improvement
                res = self_improvement.run_autonomous_self_update()
                print(json.dumps(res, indent=2))
            except Exception as e:
                print(json.dumps({"success": False, "error": str(e)}))
'''

needle = 'elif cmd == "browser_first_link" or cmd == "first_link":'
if "elif cmd == \"disk_analyze\"" not in content:
    content = content.replace(needle, cli_additions + "        " + needle, 1)
    p.write_text(content, encoding="utf-8")
    print("Updated sara_neural_brain.py successfully!")
else:
    print("Already updated.")

