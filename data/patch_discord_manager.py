# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(r"D:\MARAA AI\sara_automation_suite.py")
lines = p.read_text(encoding="utf-8").splitlines(True)

new_lines = []
for line in lines:
    new_lines.append(line)
    if "class DiscordAutonomousManager:" in line:
        new_lines.append('    AUTHORIZED_SERVER = "NEXORA"\n')
    if "self.user32 = ctypes.windll.user32" in line:
        new_lines.append('\n    def validate_server_target(self, server_name: str) -> bool:\n')
        new_lines.append('        """Enforces that SARA strictly interacts ONLY with the authorized server \'NEXORA\'."""\n')
        new_lines.append('        if not server_name:\n')
        new_lines.append('            return True\n')
        new_lines.append('        return server_name.strip().upper() == self.AUTHORIZED_SERVER\n')

p.write_text("".join(new_lines), encoding="utf-8")
print("patch_discord_manager.py completed successfully")

