# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

p = Path(r"D:\MARAA AI\SARA\resources\app\dist\server.cjs")
text = p.read_text(encoding="utf-8")

cases = re.findall(r'case\s+["\']([a-zA-Z0-9_]+)["\']\s*:', text)
unique_cases = sorted(list(set(cases)))

print(f"Total switch cases in server.cjs: {len(cases)}")
print(f"Unique switch cases: {len(unique_cases)}")

# Read all 96 tools from declarations
decl = re.findall(r'name:\s*["\']([a-zA-Z0-9_]+)["\']\s*,\s*description:', text)
decl_unique = sorted(list(set(decl)))

print(f"Total declared tools: {len(decl_unique)}")

# Compare
missing_cases = [t for t in decl_unique if t not in unique_cases]
print(f"Declared tools without direct case statement: {missing_cases}")

extra_cases = [c for c in unique_cases if c not in decl_unique]
print(f"Extra cases in switch: {extra_cases}")

