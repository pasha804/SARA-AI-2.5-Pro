# -*- coding: utf-8 -*-
from pathlib import Path

p = Path("detailed.txt")
text = p.read_text(encoding="utf-8")
text = text.replace('"server": "Pasha Dev Hub"', '"server": "NEXORA"')
text = text.replace('discord_routine "Pasha Dev Hub"', 'discord_routine "NEXORA"')
text = text.replace('"general", "announcements", "dev-chat"', '"-general-chat", "-announcements", "-ai-ml"')
text = text.replace('dev-chat channel me high-speed', '-ai-ml channel me high-speed')
p.write_text(text, encoding="utf-8")
print("detailed.txt updated successfully")

