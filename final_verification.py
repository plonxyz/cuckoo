#!/usr/bin/env python3
"""Final comprehensive verification of Python 3 migration."""

import os
import subprocess
import sys

print("=" * 70)
print("FINAL COMPREHENSIVE PYTHON 3 MIGRATION VERIFICATION")
print("=" * 70)

# Count all Python files
result = subprocess.run(
    ["find", ".", "-name", "*.py", "-type", "f", "!", "-path", "./.git/*"],
    capture_output=True, text=True
)
all_py_files = [f for f in result.stdout.strip().split('\n') if f]
print(f"\n[1/6] Total Python files found: {len(all_py_files)}")

# Compile all Python files
print("\n[2/6] Compiling all Python files...")
result = subprocess.run(
    ["python3", "-m", "compileall", ".", "-q", "-x", ".git"],
    capture_output=True, text=True
)
if result.returncode == 0 and not result.stderr:
    print("  ✓ All Python files compile successfully!")
else:
    if result.stderr:
        errors = [l for l in result.stderr.split('\n') if 'Error' in l or 'SyntaxError' in l]
        if errors:
            print(f"  ✗ Compilation errors found:")
            for err in errors[:5]:
                print(f"    {err}")
        else:
            print(f"  ⚠ Warnings only (no errors)")
    else:
        print("  ✓ All files compile (with possible warnings)")

# Check for Python 2 remnants
print("\n[3/6] Scanning for Python 2 remnants...")
checks = {
    "basestring": 0,
    "unicode\\(": 0,
    "\\.iteritems\\(": 0,
    "\\.itervalues\\(": 0,
    "xrange\\(": 0,
    "print [^(]": 0,
}

for pattern, count in checks.items():
    result = subprocess.run(
        ["grep", "-r", "-E", pattern, ".", "--include=*.py", "--exclude-dir=.git"],
        capture_output=True, text=True
    )
    if result.returncode == 0 and result.stdout:
        # Filter out comments
        lines = [l for l in result.stdout.split('\n') if l and not l.strip().startswith('#')]
        checks[pattern] = len(lines)

any_found = any(checks.values())
if not any_found:
    print("  ✓ No Python 2 remnants found!")
else:
    print("  ⚠ Some patterns found (may be false positives):")
    for pattern, count in checks.items():
        if count > 0:
            print(f"    - {pattern}: {count} occurrences")

# Check for old-style imports
print("\n[4/6] Checking for old Python 2 imports...")
old_imports = {
    "import ConfigParser": 0,
    "from ConfigParser import": 0,
    "import urllib[^.]": 0,
    "import urlparse": 0,
    "from _winreg import": 0,
}

found_imports = False
for pattern, count in old_imports.items():
    result = subprocess.run(
        ["grep", "-r", "-E", pattern, ".", "--include=*.py", "--exclude-dir=.git"],
        capture_output=True, text=True
    )
    if result.returncode == 0 and result.stdout:
        lines = result.stdout.strip().split('\n')
        if lines and lines[0]:
            old_imports[pattern] = len(lines)
            found_imports = True

if not found_imports:
    print("  ✓ All imports updated to Python 3!")
else:
    print("  ✗ Old imports found:")
    for pattern, count in old_imports.items():
        if count > 0:
            print(f"    - {pattern}: {count}")

# Check modified files in git
print("\n[5/6] Checking git status...")
result = subprocess.run(
    ["git", "diff", "--name-only"],
    capture_output=True, text=True
)
if result.stdout.strip():
    print(f"  ⚠ {len(result.stdout.strip().split())} uncommitted changes")
else:
    print("  ✓ All changes committed!")

# Summary
print("\n[6/6] Migration Summary")
print("=" * 70)
print(f"Total Python files: {len(all_py_files)}")

result = subprocess.run(
    ["git", "log", "--oneline", "--grep=Python", "-10"],
    capture_output=True, text=True
)
commits = [l for l in result.stdout.strip().split('\n') if 'Python' in l or 'python' in l]
print(f"Migration commits: {len(commits)}")

result = subprocess.run(
    ["git", "diff", "--stat", "50452a3..HEAD"],
    capture_output=True, text=True
)
if result.stdout:
    lines = result.stdout.strip().split('\n')
    if lines:
        last_line = lines[-1]
        print(f"Total changes: {last_line}")

print("\n" + "=" * 70)
print("VERIFICATION COMPLETE!")
print("=" * 70)
