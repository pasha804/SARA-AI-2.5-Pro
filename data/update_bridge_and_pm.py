# -*- coding: utf-8 -*-
import sys
import os
from pathlib import Path

# 1. Update sara_antigravity_bridge.py
bridge_path = Path(r"D:\MARAA AI\sara_antigravity_bridge.py")
b_text = bridge_path.read_text(encoding="utf-8")

old_def = 'def open_project_in_antigravity(self, project_path: str = None) -> dict:'
new_def = 'def open_project_in_antigravity(self, project_path: str = None, prompt: str = None) -> dict:'
if old_def in b_text:
    b_text = b_text.replace(old_def, new_def, 1)

old_cmd = 'cmd = f\'cmd.exe /c start "" "{self.agy_path}" --add-dir "{target}"\''
new_cmd = '''prompt_flag = f' -i "{prompt}"' if prompt else ''
            cmd = f'cmd.exe /c start "Antigravity IDE - {target.name}" "{self.agy_path}" --add-dir "{target}"{prompt_flag}\''''
if old_cmd in b_text:
    b_text = b_text.replace(old_cmd, new_cmd, 1)

bridge_path.write_text(b_text, encoding="utf-8")
print("Updated sara_antigravity_bridge.py!")

# 2. Update sara_project_manager.py
pm_path = Path(r"D:\MARAA AI\sara_project_manager.py")
pm_text = pm_path.read_text(encoding="utf-8")

old_root = 'projects_root = WORKSPACE_ROOT / "projects"'
new_root = '''desktop_dir = Path(os.environ.get("USERPROFILE") or os.path.expanduser("~")).resolve() / "Desktop"
        projects_root = desktop_dir / "pasha_nexus_dashboard"
        p_dir = projects_root'''

if old_root in pm_text:
    pm_text = pm_text.replace(old_root, new_root, 1)

old_launch = 'agy_res = bridge.open_project_in_antigravity(str(p_dir))'
new_launch = '''prompt_text = f"Pasha Jan requested full-stack SaaS platform '{project_name}' ({project_type}). Review AGENTS.md, verify server.py API endpoints, and ensure 100% test pass on test_project.py."
            agy_res = bridge.open_project_in_antigravity(str(p_dir), prompt=prompt_text)'''

if old_launch in pm_text:
    pm_text = pm_text.replace(old_launch, new_launch, 1)

pm_path.write_text(pm_text, encoding="utf-8")
print("Updated sara_project_manager.py!")

