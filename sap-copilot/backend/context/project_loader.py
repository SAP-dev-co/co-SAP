# project_loader.py

import os  # Provides functions to work with file paths and directories — essential for resolving and comparing absolute paths. 🔺High
import ast  # Used to parse Python files and extract their import statements safely and reliably via abstract syntax trees. 🔺High
from typing import Set, Dict, List  # Enables clearer type hinting for input/output — improves readability and debugging clarity. 🟡Medium

from context import pylint_runner  # Imports the module responsible for running pylint and collecting static analysis results. 🔺High

def get_imported_files(file_path: str, project_root: str) -> Set[str]:
    """
    Parses a Python file and collects the absolute paths of all imported modules within the project root.
    This supports identifying only local imports, not external libraries.
    """
    imported_files = set()  # A set to store unique file paths that were imported by the current file. 🔺High

    try:
        with open(file_path, "r") as f:  # Opens the file in read mode to parse its content into an AST. 🔺High
            tree = ast.parse(f.read(), filename=file_path)  # Parses file content into an abstract syntax tree for analysis. 🔺High

        for node in ast.walk(tree):  # Walks through every node in the syntax tree to find import statements. 🔺High
            if isinstance(node, ast.Import):  # Detects general 'import module' statements. 🟡Medium
                for alias in node.names:
                    path = resolve_module_to_path(alias.name, project_root)  # Resolves module name to a file path within root. 🔺High
                    if path:
                        imported_files.add(path)  # Adds resolved paths if they exist (filters out stdlib/external packages). 🔺High
            elif isinstance(node, ast.ImportFrom):  # Detects 'from module import ...' style imports. 🟡Medium
                module = node.module
                if module:
                    path = resolve_module_to_path(module, project_root)  # Same resolution logic applies here. 🔺High
                    if path:
                        imported_files.add(path)

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")  # Handles syntax errors or I/O issues gracefully — helps debugging. 🟡Medium

    return imported_files  # Returns all local imported file paths that will be recursively scanned. 🔺High

def resolve_module_to_path(module: str, root: str) -> str:
    """
    Resolves an import like 'utils.helpers' to a real file path such as 'root/utils/helpers.py'.
    """
    path = os.path.join(root, *module.split(".")) + ".py"  # Converts dot notation into actual file path in the project. 🔺High
    return path if os.path.exists(path) else None  # Ensures file actually exists before adding it to scan list. 🔺High

def recursive_scan(entry_file: str, project_root: str) -> Dict[str, List[dict]]:
    """
    Recursively scans a file and its local imports for pylint errors until no new files with errors are found.
    """
    scanned_files = set()  # Tracks files that have already been scanned to avoid duplication and infinite loops. 🔺High
    error_map = {}  # Stores error results from pylint organized by file. 🔺High
    to_scan = {os.path.abspath(entry_file)}  # Begins with the user-selected file, resolved to absolute path. 🔺High

    while to_scan:
        current_batch = to_scan - scanned_files  # Isolates only the files that have not yet been analyzed. 🔺High

        if not current_batch:
            break  # If there are no new files to scan, exit the loop. 🔺High

        batch_errors = pylint_runner.run_pylint(list(current_batch))  # Runs pylint on the current batch of unscanned files. 🔺High
        error_map.update(batch_errors)  # Adds error results to the central error map. 🔺High
        scanned_files.update(current_batch)  # Marks these files as scanned. 🔺High

        new_files = set()  # Temporary set to hold new imports discovered in files with errors. 🔺High
        for file in batch_errors:  # We only analyze files that had actual errors. This limits unnecessary scanning. 🔺High
            imports = get_imported_files(file, project_root)  # Parses imports only from files that had errors. 🔺High
            new_files.update(imports)  # Adds these imports to the pool of files to potentially scan next. 🔺High

        to_scan.update(new_files)  # Expands the scan frontier with newly discovered dependent files. 🔺High

    return error_map  # Final output: mapping of files → list of pylint errors for use by LangGraph or frontends. 🔺High
