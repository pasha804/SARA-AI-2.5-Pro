# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

server_cjs = Path(r"D:\MARAA AI\SARA\resources\app\dist\server.cjs")
content = server_cjs.read_text(encoding="utf-8")

# Find tools defined with name and description
matches = re.findall(r'name:\s*["\']([a-zA-Z0-9_]+)["\']\s*,\s*description:', content)
tools_unique = sorted(list(set(matches)))

print(f"Total tools in server.cjs: {len(tools_unique)}")
print(json.dumps(tools_unique, indent=2))

