import subprocess  # Used to run shell commands like 'pylint' from within Python scripts. Enables automation of linting. 🔺High
import json  # Used to parse pylint's output when formatted as JSON, allowing structured and readable error data. 🔺High
from typing import List, Dict, Any  # Provides type hints to improve code clarity and editor support — not strictly required but helpful. 🟡Medium


def run_pylint(file_paths: List[str]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Runs pylint on the given list of Python file paths and returns a dictionary of issues grouped by file.
    """

    if not file_paths:  # Prevents unnecessary execution if input list is empty — saves computation and avoids subprocess errors. 🔺High
        return {}

    command = [  # Constructs the pylint command line call, specifying that output should be returned in machine-readable JSON format. 🔺High
        "pylint",
        "--output-format=json",  # Ensures that pylint outputs data in JSON which is easier to parse and work with in Python. 🔺High
        *file_paths  # Dynamically inserts all file paths as separate arguments into the command. 🔺High
    ]

    try:
        result = subprocess.run(  # Executes the constructed pylint command and captures its output and error streams. 🔺High
            command,
            capture_output=True,  # Ensures both stdout and stderr are caught by Python for later processing or error handling. 🔺High
            text=True  # Converts byte stream output to string automatically for easier parsing and display. 🔺High
        )

        output = result.stdout  # Stores the output from pylint, which should be a JSON array as a string. 🔺High

        messages = json.loads(output)  # Parses the JSON string output into a Python list of dictionaries (1 per error/warning). 🔺High

        errors_by_file = {}  # Initializes an empty dictionary to group all errors by their originating file. 🔺High

        for msg in messages:  # Iterates over each individual pylint message to organize them by file. 🔺High
            path = msg.get("path")  # Extracts the file path where the issue occurred from the message object. 🔺High
            if path not in errors_by_file:
                errors_by_file[path] = []  # Creates a new list for errors from this file if not already present. 🔺High
            errors_by_file[path].append({  # Appends the relevant error details for this file entry. 🔺High
                "type": msg.get("type"),  # Type of message: error, warning, refactor, etc. 🔺High
                "module": msg.get("module"),  # Python module name for where the error occurred. 🟡Medium
                "obj": msg.get("obj"),  # Function, method, or class name related to the error (if applicable). 🟡Medium
                "line": msg.get("line"),  # Line number in the file where the issue was found. 🔺High
                "column": msg.get("column"),  # Column number on the line where the issue begins. 🔺High
                "message": msg.get("message"),  # Human-readable description of what went wrong. 🔺High
                "symbol": msg.get("symbol")  # Symbolic ID like 'unused-import' for rule classification. 🔺High
            })

        return errors_by_file  # Returns the full dictionary mapping each file to a list of linting issues found. 🔺High

    except json.JSONDecodeError as e:  # Handles unexpected formatting or broken output from pylint by catching JSON parsing errors. 🔺High
        print("Failed to parse pylint output:", e)  # Helps diagnose why pylint output could not be parsed as JSON. 🟡Medium
        print("Raw output:\n", result.stdout)  # Prints raw output for debugging — especially useful during development or CI failures. 🟡Medium
        return {}

    except Exception as e:  # Catches any other exceptions that might occur during subprocess or parsing. 🔺High
        print("Unexpected error while running pylint:", e)  # Gives visibility into unexpected failures during execution. 🟡Medium
        return {}
