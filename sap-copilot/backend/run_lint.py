import os
from backend.analyzer import analyze_code_string

def lint_all_py_files(directory):
    lint_reports = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    code = f.read()
                report = analyze_code_string(code)
                lint_reports[filepath] = report
    return lint_reports

if __name__ == "__main__":
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    reports = lint_all_py_files(backend_dir)

    errors_found = False
    for file, report in reports.items():
        print(f"\nLint results for {file}:\n")
        print(report)
        if "error" in report.lower() or "fatal" in report.lower():
            errors_found = True

    if errors_found:
        print("\nSome files have lint errors. Exiting.")
        exit(1)

    print("\nAll files passed lint checks. Running main app...")