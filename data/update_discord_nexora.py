# -*- coding: utf-8 -*-
from pathlib import Path

# 1. Update sara_neural_brain.py
brain_p = Path(r"D:\MARAA AI\sara_neural_brain.py")
b_text = brain_p.read_text(encoding="utf-8")
b_text = b_text.replace('srv = sys.argv[2] if len(sys.argv) > 2 else "Pasha Dev Hub"', 'srv = "NEXORA"')
brain_p.write_text(b_text, encoding="utf-8")
print("sara_neural_brain.py updated.")

# 2. Update server.cjs
server_p = Path(r"D:\MARAA AI\SARA\resources\app\dist\server.cjs")
s_text = server_p.read_text(encoding="utf-8")
s_text = s_text.replace('args.server_name || "Pasha Dev Hub"', 'args.server_name || "NEXORA"')
s_text = s_text.replace('description: "Name of the Discord server (e.g. Pasha Dev Hub)."', 'description: "Name of the Discord server (strictly locked to authorized server NEXORA)."')
server_p.write_text(s_text, encoding="utf-8")
print("server.cjs updated.")

# 3. Update SARA app duplicate if present
sara_app_brain = Path(r"D:\MARAA AI\SARA\resources\app\sara_neural_brain.py")
if sara_app_brain.exists():
    ab_text = sara_app_brain.read_text(encoding="utf-8")
    ab_text = ab_text.replace('srv = sys.argv[2] if len(sys.argv) > 2 else "Pasha Dev Hub"', 'srv = "NEXORA"')
    sara_app_brain.write_text(ab_text, encoding="utf-8")
    print("SARA/resources/app/sara_neural_brain.py updated.")
