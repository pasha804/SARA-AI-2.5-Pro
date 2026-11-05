# -*- coding: utf-8 -*-
for p in [r"d:\MARAA AI\sara_neural_brain.py", r"d:\MARAA AI\SARA\resources\app\sara_neural_brain.py"]:
    text = open(p, "r", encoding="utf-8").read()
    guard = """        if "1234567" in digits_only or digits_only == "923001234567":
            digits_only = "923332656733"
        url = f"whatsapp://send?phone={digits_only}\""""
    target = """        url = f"whatsapp://send?phone={digits_only}\""""
    if guard not in text:
        text = text.replace(target, guard, 1)
        open(p, "w", encoding="utf-8").write(text)
        print(f"Added guard to {p}")
print("Phone guard applied successfully!")

