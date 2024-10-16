import ast

def parse_code_file(filename):
    """Parses a Python code file and returns a list of imported packages.

    Args:
    filename: The path to the Python code file.

    Returns:
    A list of imported package names.
    """

    with open(filename, 'r') as f:
        tree = ast.parse(f.read())

    imported_packages = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_packages.extend([name.name for name in node.names])
        elif isinstance(node, ast.ImportFrom):
            imported_packages.extend([name.name for name in node.names])

    return imported_packages

def process_files(filenames, output_file="requirements.txt"):
  """Processes a list of Python code files and writes combined imports to a file.

  Args:
    filenames: A list of paths to Python code files.
    output_file: The name of the output file to write the combined imports (default: requirements.txt).
  """

  all_packages = set()
  for filename in filenames:
    all_packages.update(parse_code_file(filename))

  with open(output_file, 'w') as f:
    for package in all_packages:
      f.write(f"{package}\n")


# Example usage
code_files = ["deployed_ml_app.py", "helper_functions.py"]  # List your file paths here
process_files(code_files)
print(f"Imported packages from all files written to {output_file} (versions not included).")