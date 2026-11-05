# -*- coding: utf-8 -*-
p = r"D:\MARAA AI\sara_project_manager.py"
text = open(p, "r", encoding="utf-8").read()
old = """        desktop_dir = Path(os.environ.get("USERPROFILE") or os.path.expanduser("~")).resolve() / "Desktop"
        projects_root = desktop_dir / "pasha_nexus_dashboard"
        p_dir = projects_root
        p_dir.mkdir(parents=True, exist_ok=True)
        p_dir = projects_root / project_name"""
new = """        desktop_dir = Path(os.environ.get("USERPROFILE") or os.path.expanduser("~")).resolve() / "Desktop"
        p_dir = desktop_dir / project_name"""
if old in text:
    text = text.replace(old, new, 1)
else:
    # Check if variant exists
    text = text.replace('projects_root = desktop_dir / "pasha_nexus_dashboard"\n        p_dir = projects_root', 'p_dir = desktop_dir / project_name')
open(p, "w", encoding="utf-8").write(text)
print("Updated project path cleanly!")

