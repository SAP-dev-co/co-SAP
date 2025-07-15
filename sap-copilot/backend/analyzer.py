from pylint.lint import Run   
from io import StringIO
import contextlib
import tempfile
import os
import sys 
from pathlib import Path

def analyze_code_string(code: str) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
        tmp.write(code.encode())
        temp_path = tmp.name

    pylint_output = StringIO()
    try:
        with contextlib.redirect_stdout(pylint_output):
            Run([temp_path], exit=False)
    finally:
        os.unlink(temp_path)
    return pylint_output.getvalue()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyzer.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    code = Path(file_path).read_text(encoding="utf-8")
    result = analyze_code_string(code)
    print(result)