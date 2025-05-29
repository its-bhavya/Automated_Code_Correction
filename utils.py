# utils.py

import subprocess
from pathlib import Path

def load_code(path):
    with open(path, "r") as f:
        return f.read()

def save_code(path, code):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(code)

import pytest
import io
from contextlib import redirect_stdout

def validate_fix_with_tester(algo_name, flag):
    """Run tester.py and return True if fixed code passes all tests, else False."""

    # Run tester.py with the algorithm name as argument
    result = subprocess.run(
        ["python", "tester.py", algo_name, flag],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Capture full output (stdout + stderr)
    output = result.stdout + "\n" + result.stderr

    for line in output.splitlines():
        if "Passed:" in line:
            parts = line.split(":")[1].strip().split("/")
            passed = int(parts[0])
            total = int(parts[1])
            print(f"Total test cases passed = {passed}/{total}")
            return passed == total, passed, total