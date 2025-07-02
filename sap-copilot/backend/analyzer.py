from pylint.lint import Run   
from io import StringIO
import contextlib
import tempfile
import os

def analyze_code_string(code: str) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
        tmp.write(code.encode())
        temp_path = tmp.name

    pylint_output = StringIO()
    try:
        with contextlib.redirect_stdout(pylint_output):
            Run([temp_path], do_exit=False)
    finally:
        os.unlink(temp_path)
    return pylint_output.getvalue()
