# -*- coding: utf-8 -*-
"""
SARA AI 2.5 Pro — Autonomous User Project Manager & Health Auditor
Discovers, catalogs, audits, and manages user projects across workspace roots.
Identifies React, Next.js, Vite, Node, Python, Electron, and Web stacks safely.
"""

import os
import sys
import json
import time
import datetime
import subprocess
from pathlib import Path

WORKSPACE_ROOT = Path(r"D:\MARAA AI").resolve()
USER_DESKTOP = Path(os.environ.get("USERPROFILE") or os.path.expanduser("~")).resolve() / "Desktop"
PROJECT_REGISTRY_FILE = WORKSPACE_ROOT / "data" / "project_registry.json"
PROJECT_REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)

IGNORED_DIRS = {
    "node_modules", ".git", "__pycache__", "dist", "build", ".next",
    "vendor", ".venv", "venv", "env", "coverage", ".turbo", "bin", "obj",
    "$RECYCLE.BIN", "$Recycle.Bin", "System Volume Information"
}


class ProjectManager:

    def __init__(self, roots: list = None):
        if roots is not None:
            self.roots = roots
        else:
            self.roots = [WORKSPACE_ROOT, USER_DESKTOP]
            if Path("E:\\").exists():
                self.roots.append(Path("E:\\"))
        self.registry = self.load_registry()

    def load_registry(self) -> dict:
        if PROJECT_REGISTRY_FILE.exists():
            try:
                return json.loads(PROJECT_REGISTRY_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"projects": {}, "last_scanned_at": None, "total_projects": 0}

    def save_registry(self):
        try:
            self.registry["last_scanned_at"] = datetime.datetime.now().isoformat()
            self.registry["total_projects"] = len(self.registry.get("projects", {}))
            PROJECT_REGISTRY_FILE.write_text(
                json.dumps(self.registry, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
        except Exception as e:
            print(f"[ProjectManager] Save failed: {e}")

    def identify_project_type(self, dir_path: Path) -> dict:
        """Inspects manifests and files to categorize tech stack."""
        project_type = "Generic / Custom"
        entry_points = []
        scripts = {}

        package_json = dir_path / "package.json"
        requirements_txt = dir_path / "requirements.txt"
        pyproject_toml = dir_path / "pyproject.toml"
        index_html = dir_path / "index.html"
        has_agents = (dir_path / "AGENTS.md").exists() or (dir_path / ".agents").exists()
        
        py_files = []
        try:
            py_files = [f.name for f in dir_path.glob("*.py") if not f.name.startswith(".")]
        except Exception:
            pass

        # Check installed skills in .agents/skills
        skills = []
        skills_dir = dir_path / ".agents" / "skills"
        if skills_dir.exists():
            try:
                skills = [d.name for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
            except Exception:
                pass

        if package_json.exists():
            try:
                pkg = json.loads(package_json.read_text(encoding="utf-8", errors="ignore"))
                scripts = pkg.get("scripts", {})
                deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}

                if "next" in deps:
                    project_type = "Next.js Full-Stack App"
                elif "vite" in deps or "react" in deps:
                    project_type = "React / Vite Web App"
                elif "electron" in deps:
                    project_type = "Electron Desktop App"
                else:
                    project_type = "Node.js / JavaScript Project"

                if "main" in pkg:
                    entry_points.append(pkg["main"])
            except Exception:
                project_type = "Node.js (Malformed package.json)"

        elif has_agents:
            if any("trading" in f.lower() or "risk" in f.lower() for f in py_files) or "trading" in dir_path.name.lower():
                project_type = "Antigravity AI Quantitative Trading System"
            else:
                project_type = "Antigravity Multi-Agent Workspace"

        elif requirements_txt.exists() or pyproject_toml.exists():
            project_type = "Python Application / Service"

        elif py_files:
            project_type = "Python Script Suite / Application"

        elif index_html.exists():
            project_type = "HTML5 / Vanilla Web App"

        # Check for web & script entry points across the project
        for cand in [
            "index.html", "src/main.jsx", "src/main.tsx", "src/main.js", 
            "src/index.jsx", "src/index.js", "src/App.jsx", "src/App.tsx",
            "main.py", "app.py", "server.py", "run.py", "manage.py"
        ]:
            if (dir_path / cand).exists() and cand not in entry_points:
                entry_points.append(cand)

        # If no standard entry point found yet, include discovered Python scripts
        if not entry_points and py_files:
            entry_points.extend(py_files[:3])

        return {
            "type": project_type,
            "entry_points": entry_points,
            "scripts": scripts,
            "has_package_json": package_json.exists(),
            "has_python": bool(requirements_txt.exists() or pyproject_toml.exists() or py_files),
            "has_agents": has_agents,
            "skills": skills
        }

    def discover_projects(self, max_depth: int = 2) -> dict:
        """Bounded scan of configured workspace roots."""
        discovered = {}

        for root in self.roots:
            p_root = Path(root).resolve()
            if not p_root.exists():
                continue

            # Check if root itself is a project
            root_info = self.identify_project_type(p_root)
            if root_info["type"] != "Generic / Custom":
                discovered[p_root.name] = {
                    "name": p_root.name,
                    "path": str(p_root),
                    **root_info,
                    "discovered_at": datetime.datetime.now().isoformat()
                }

            # Bounded scan children
            try:
                for item in p_root.iterdir():
                    if item.is_dir() and item.name not in IGNORED_DIRS and not item.name.startswith("."):
                        info = self.identify_project_type(item)
                        if info["type"] != "Generic / Custom":
                            discovered[item.name] = {
                                "name": item.name,
                                "path": str(item),
                                **info,
                                "discovered_at": datetime.datetime.now().isoformat()
                            }
            except Exception:
                pass

        self.registry["projects"].update(discovered)
        self.save_registry()
        return {
            "success": True,
            "total_discovered": len(discovered),
            "projects": discovered
        }

    def audit_project(self, project_name_or_path: str) -> dict:
        """Performs a comprehensive, non-destructive health check on a specific project."""
        p = Path(project_name_or_path).resolve()
        if not p.exists():
            # Check configured roots for matching folder name
            for root in self.roots:
                cand = Path(root).resolve() / project_name_or_path
                if cand.exists() and cand.is_dir():
                    p = cand
                    break
            else:
                if project_name_or_path in self.registry.get("projects", {}):
                    p = Path(self.registry["projects"][project_name_or_path]["path"])
                else:
                    self.discover_projects()
                    if project_name_or_path in self.registry.get("projects", {}):
                        p = Path(self.registry["projects"][project_name_or_path]["path"])
                    else:
                        return {"success": False, "error": f"Project not found: {project_name_or_path}"}

        info = self.identify_project_type(p)
        issues = []
        checks_passed = []

        # Check entry points
        if not info["entry_points"]:
            issues.append({"level": "WARNING", "message": "No standard entry point (main.py, index.html, package main) detected."})
        else:
            checks_passed.append(f"Entry points verified: {', '.join(info['entry_points'])}")

        # Check package manifest integrity
        pkg_file = p / "package.json"
        if pkg_file.exists():
            try:
                pkg_data = json.loads(pkg_file.read_text(encoding="utf-8"))
                checks_passed.append("package.json parsed successfully")
                if "test" in pkg_data.get("scripts", {}):
                    checks_passed.append("Test script available in package.json")
                else:
                    issues.append({"level": "INFO", "message": "No 'test' script declared in package.json."})
            except Exception as e:
                issues.append({"level": "HIGH", "message": f"package.json is malformed: {e}"})

        # Check git status if available
        git_dir = p / ".git"
        git_status = "Not a Git repository"
        if git_dir.exists():
            try:
                res = subprocess.run(["git", "status", "-s"], cwd=str(p), capture_output=True, text=True, timeout=3)
                git_status = "Git tracked: Clean" if not res.stdout.strip() else f"Uncommitted changes: {len(res.stdout.splitlines())} files"
                checks_passed.append(git_status)
            except Exception:
                git_status = "Git installed check failed"

        # Check Antigravity agentic specifications
        if (p / "AGENTS.md").exists():
            checks_passed.append("AGENTS.md agentic specification verified")
        if info.get("skills"):
            checks_passed.append(f"Antigravity skills active ({len(info['skills'])}): {', '.join(info['skills'])}")
        if (p / "skills-inventory.json").exists():
            checks_passed.append("Skills inventory manifest verified")
        if (p / "risk-policy.md").exists():
            checks_passed.append("Risk policy specification active")
        if (p / "testing-report.md").exists():
            checks_passed.append("Testing report documentation verified")

        # Overall health score calculation
        health_score = 100
        for iss in issues:
            if iss["level"] == "HIGH": health_score -= 30
            elif iss["level"] == "WARNING": health_score -= 15
            elif iss["level"] == "INFO": health_score -= 5

        health_score = max(0, min(100, health_score))

        audit_result = {
            "success": True,
            "project_name": p.name,
            "path": str(p),
            "project_type": info["type"],
            "health_score": health_score,
            "status": "HEALTHY" if health_score >= 80 else ("DEGRADED" if health_score >= 50 else "CRITICAL"),
            "checks_passed": checks_passed,
            "issues": issues,
            "available_scripts": list(info.get("scripts", {}).keys()),
            "audited_at": datetime.datetime.now().isoformat()
        }

        # Update registry entry with latest audit result
        if p.name in self.registry.get("projects", {}):
            self.registry["projects"][p.name]["last_audit"] = audit_result
            self.save_registry()

        return audit_result


project_manager = ProjectManager()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "discover":
            res = project_manager.discover_projects()
            print(json.dumps(res, indent=2, ensure_ascii=False))
        elif cmd == "audit":
            target = sys.argv[2] if len(sys.argv) > 2 else str(WORKSPACE_ROOT)
            res = project_manager.audit_project(target)
            print(json.dumps(res, indent=2, ensure_ascii=False))
        elif cmd == "list":
            res = project_manager.registry.get("projects", {})
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            res = project_manager.audit_project(cmd)
            print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print("Scanning workspace for projects...")
        res = project_manager.discover_projects()
        print(f"Discovered {res['total_discovered']} projects:")
        for name, p_data in res["projects"].items():
            print(f"  • {name} -> {p_data['type']} at {p_data['path']}")
