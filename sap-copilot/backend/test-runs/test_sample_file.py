from backend.analyzer import analyze_code_string

with open("backend/sample_code.py", "r", encoding="utf-8") as f:
    code = f.read()

result = analyze_code_string(code)

print("Lint results for sample_code.py:\n")
print(result)

if "error" in result.lower() or "fatal" in result.lower():
    print("\n Issues detected")
else:
    print("\n No issues")