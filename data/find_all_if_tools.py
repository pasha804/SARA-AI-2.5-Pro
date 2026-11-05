# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

p = Path(r"D:\MARAA AI\SARA\resources\app\dist\server.cjs")
text = p.read_text(encoding="utf-8")

matches = re.findall(r'tool\s*===?\s*["\']([a-zA-Z0-9_]+)["\']', text)
tools_handled = sorted(list(set(matches)))

print(f"Total tools handled with `if (tool === ...)` in server.cjs: {len(tools_handled)}")
print(json.dumps(tools_handled, indent=2))

