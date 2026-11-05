p = r"D:\MARAA AI\sara_neural_brain.py"
with open(p, "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(len(lines)):
    if 'elif cmd == "discord_routine"' in lines[i]:
        lines[i] = '        elif cmd == "discord_routine" or cmd == "discord_engagement":\n'
with open(p, "w", encoding="utf-8") as f:
    f.writelines(lines)
print("Indentation fixed in sara_neural_brain.py!")

