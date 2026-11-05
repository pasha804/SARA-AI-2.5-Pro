# -*- coding: utf-8 -*-
import re
from pathlib import Path

p = Path(r"D:\MARAA AI\SARA\resources\app\dist\server.cjs")
text = p.read_text(encoding="utf-8")

decl_names = re.findall(r'name:\s*["\']([a-zA-Z0-9_]+)["\']', text)
tool_cases = re.findall(r'tool\s*===?\s*["\']([a-zA-Z0-9_]+)["\']', text)

# Also check tools in sara_neural_brain.py
brain_path = Path(r"D:\MARAA AI\sara_neural_brain.py")
brain_text = brain_path.read_text(encoding="utf-8")
brain_cmds = re.findall(r'cmd\s*==\s*["\']([a-zA-Z0-9_]+)["\']', brain_text)

all_server_tools = sorted(list(set(decl_names + tool_cases)))
all_brain_tools = sorted(list(set(brain_cmds)))

print(f"Total unique tools in server.cjs: {len(all_server_tools)}")
print(f"Total unique commands in sara_neural_brain.py: {len(all_brain_tools)}")
combined = sorted(list(set(all_server_tools + all_brain_tools)))
print(f"Total distinct SARA tools combined: {len(combined)}")
for i, t in enumerate(combined, 1):
    print(f"{i:2d}. {t}")

