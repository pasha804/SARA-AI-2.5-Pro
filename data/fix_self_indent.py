p = r"D:\MARAA AI\sara_self_improvement.py"
with open(p, "r", encoding="utf-8") as f:
    content = f.read()

bad = """    else:
    report = self_improvement.evaluate_system_capabilities()
    print("Self-Improvement Assessment Report:")
    print(json.dumps(report, indent=2))"""

good = """    else:
        report = self_improvement.evaluate_system_capabilities()
        print("Self-Improvement Assessment Report:")
        print(json.dumps(report, indent=2))"""

content = content.replace(bad, good)
with open(p, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed indentation in sara_self_improvement.py!")

