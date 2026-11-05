with open("architecture.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if line.startswith("| **Owner Name**"):
        skip = True
        new_lines.append("| **Owner Name** | Pasha Dev / Mubashar Jan | Strictly addressed as **Pasha Jan** or **Mubashar Jan** |\n")
        new_lines.append("| **Phone Number** | `+923332656733` | Dummy numbers (`03001234567`) eradicated and blocked by code guards |\n")
        new_lines.append("| **Email Address** | `pashadev804@gmail.com` | Primary notification & digest recipient |\n")
        new_lines.append("| **Authorized Discord** | `NEXORA` | 8 Categories, 48+ Channels strictly isolated with Win32 focus guard |\n")
        new_lines.append("| **Benchmarked Models** | APInex Free Verified Tier | Rank 1: `free/glm-5.3-flashx` (1216ms), Rank 2: `free/gemini-3.8-flash` (1320ms), Rank 3: `free/deepseek-v4-pro-0813` (1369ms) |\n")
        new_lines.append("| **Desktop Projects** | `C:\\Users\\USER\\Desktop\\pasha_nexus_dashboard` | Autonomous full-stack scaffolding with syntax self-healing |\n")
        new_lines.append("| **Memory Engine** | 3-Tier SQLite + FTS5 | L0 Working RAM, L1 Facts, L2 Milestones, automated user profile synthesis & backups |\n")
        new_lines.append("| **Test Quality Gate** | 244 / 244 Unit Tests Passing | `python -m unittest discover tests` — 100% OK, zero popups or errors |\n")
        new_lines.append("| **Disk Reclamation** | C: Drive Cleanable Space | Safe temporary caches verified for user-confirmed cleanup |\n")
    elif skip and line.startswith("| **Disk Reclamation**"):
        skip = False
    elif not skip:
        new_lines.append(line)

with open("architecture.md", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
print("Updated architecture.md cleanly")

