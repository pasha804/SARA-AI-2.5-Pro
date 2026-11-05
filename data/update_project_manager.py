# -*- coding: utf-8 -*-
p = r"D:\MARAA AI\sara_project_manager.py"
with open(p, "r", encoding="utf-8") as f:
    content = f.read()

cli_target = '        if cmd == "discover":'
cli_replacement = '''        if cmd == "create":
            name = sys.argv[2] if len(sys.argv) > 2 else "pasha_nexus_dashboard"
            p_type = sys.argv[3] if len(sys.argv) > 3 else "Full-Stack SaaS Platform"
            res = project_manager.create_autonomous_project(name, p_type)
            print(json.dumps(res, indent=2, ensure_ascii=False))
        elif cmd == "resolve":
            target = sys.argv[2] if len(sys.argv) > 2 else str(WORKSPACE_ROOT / "projects" / "pasha_nexus_dashboard")
            res = project_manager.resolve_project_errors(target)
            print(json.dumps(res, indent=2, ensure_ascii=False))
        elif cmd == "discover":'''

content = content.replace(cli_target, cli_replacement, 1)
with open(p, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated CLI in sara_project_manager.py successfully!")
