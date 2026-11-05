# -*- coding: utf-8 -*-
for p in [
    r"D:\MARAA AI\SARA\resources\app\dist\assets\jarvis_hud.js",
    r"D:\MARAA AI\SARA\resources\app\assets\jarvis_hud.js"
]:
    try:
        with open(p, "r", encoding="utf-8") as f:
            text = f.read()
        text = text.replace("Pasha Dev", "Pasha Jan")
        text = text.replace("Good Evening, Pasha Dev", "Good Evening, Pasha Jan")
        text = text.replace("AI Assistant", "Neural Copilot")
        text = text.replace("Research completed\n              AI models 2026", "Pipelines active\n              360+ N8N Automations")
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Updated {p} successfully!")
    except Exception as e:
        print(f"Error updating {p}: {e}")

