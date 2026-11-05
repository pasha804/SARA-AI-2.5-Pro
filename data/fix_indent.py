p = r"D:\MARAA AI\sara_automation_suite.py"
with open(p, "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(len(lines)):
    if 'elif pipeline in ["discord_routine"' in lines[i]:
        lines[i] = '        elif pipeline in ["discord_routine", "discord_engagement"]:\n'
with open(p, "w", encoding="utf-8") as f:
    f.writelines(lines)
print("Indentation normalized successfully!")

