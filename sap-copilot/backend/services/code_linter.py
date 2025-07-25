from pylint.lint import Run
from io import StringIO
import tempfile
import os
import contextlib

def run_pylint_on_code(code: str) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
        tmp.write(code.encode())
        temp_path = tmp.name

        output = StringIO()
        try:
            with contextlib.redirect_stdout(output):
                Run([temp_path], exit=False)
        finally:
            os.unlink(temp_path)
        return output.getvalue() #this is the scan report from pylint

def analyze_multiple_files(files: dict) -> str:
    reports = []
    for filename, content in files.items():
        try:
            report = run_pylint_on_code(content)
            reports.append(f"###{filename}:\n{report}")
        except Exception as e:
            reports.append(f"###{filename}:\nError during analysis:{str(e)}")
    return "\n\n".join(reports)
