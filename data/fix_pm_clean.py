# -*- coding: utf-8 -*-
p = r"D:\MARAA AI\sara_project_manager.py"
text = open(p, "r", encoding="utf-8").read()
old = """        desktop_dir = Path(os.environ.get("USERPROFILE") or os.path.expanduser("~")).resolve() / "Desktop"
        p_dir = desktop_dir / project_name
        projects_root.mkdir(parents=True, exist_ok=True)
        p_dir = projects_root / project_name
        p_dir.mkdir(parents=True, exist_ok=True)
        (p_dir / "src").mkdir(parents=True, exist_ok=True)"""
new = """        desktop_dir = Path(os.environ.get("USERPROFILE") or os.path.expanduser("~")).resolve() / "Desktop"
        p_dir = desktop_dir / project_name
        p_dir.mkdir(parents=True, exist_ok=True)
        (p_dir / "src").mkdir(parents=True, exist_ok=True)"""
text = text.replace(old, new, 1)
open(p, "w", encoding="utf-8").write(text)
print("Fixed lines 293-298!")

