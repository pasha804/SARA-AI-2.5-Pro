# -*- coding: utf-8 -*-
from pathlib import Path
import re

p = Path(r"D:\MARAA AI\SARA\resources\app\dist\server.cjs")
text = p.read_text(encoding="utf-8")

matches = [m.start() for m in re.finditer(r'systemInfo|analyzeCDriveSpace|openWhatsAppChat', text)]
for idx in matches[:5]:
    print("--- MATCH AT", idx, "---")
    print(text[idx-40:idx+200])

