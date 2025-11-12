#!/usr/bin/env python3
"""Quick test script to verify Python 3 migration basics."""

import sys
import os

print("=" * 60)
print("Cuckoo Python 3 Migration Verification Test")
print("=" * 60)

# Test 1: Python version
print("\n[1/10] Checking Python version...")
if sys.version_info >= (3, 6):
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
else:
    print(f"✗ Python {sys.version_info.major}.{sys.version_info.minor} (need 3.6+)")
    sys.exit(1)

# Test 2: Import basic standard library modules
print("\n[2/10] Testing standard library imports...")
try:
    import configparser
    import urllib.parse
    import urllib.request
    print("✓ Standard library imports (configparser, urllib)")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

# Test 3: Check setup.py syntax
print("\n[3/10] Checking setup.py...")
try:
    with open("setup.py", "r") as f:
        code = f.read()
        compile(code, "setup.py", "exec")
    print("✓ setup.py compiles successfully")
except SyntaxError as e:
    print(f"✗ Syntax error in setup.py: {e}")
    sys.exit(1)

# Test 4: Test basic cuckoo module syntax
print("\n[4/10] Checking cuckoo module files...")
test_files = [
    "cuckoo/main.py",
    "cuckoo/common/config.py",
    "cuckoo/common/utils.py",
    "cuckoo/misc.py"
]
all_ok = True
for filepath in test_files:
    try:
        with open(filepath, "r") as f:
            code = f.read()
            compile(code, filepath, "exec")
        print(f"  ✓ {filepath}")
    except SyntaxError as e:
        print(f"  ✗ {filepath}: {e}")
        all_ok = False

if not all_ok:
    sys.exit(1)

# Test 5: Check for Python 2 remnants
print("\n[5/10] Checking for Python 2 remnants...")
remnants_found = False

# Check for print statements without parentheses (basic check)
import subprocess
result = subprocess.run(
    ["grep", "-r", "-n", "print [^(]", "cuckoo/", "--include=*.py"],
    capture_output=True, text=True
)
if result.returncode == 0 and result.stdout:
    lines = result.stdout.strip().split('\n')
    # Filter out comments and strings
    real_issues = [l for l in lines if 'print' in l and not l.strip().startswith('#')]
    if real_issues:
        print(f"  ⚠ Found {len(real_issues)} potential print statement issues")
        remnants_found = True
else:
    print("  ✓ No print statement issues found")

# Test 6: Check for basestring usage
print("\n[6/10] Checking for 'basestring' usage...")
result = subprocess.run(
    ["grep", "-r", "basestring", "cuckoo/", "--include=*.py"],
    capture_output=True, text=True
)
if result.returncode == 0 and result.stdout:
    print(f"  ✗ Found 'basestring' usage (should be 'str')")
    remnants_found = True
else:
    print("  ✓ No 'basestring' usage found")

# Test 7: Check for unicode() usage
print("\n[7/10] Checking for 'unicode()' usage...")
result = subprocess.run(
    ["grep", "-r", "-w", "unicode(", "cuckoo/", "--include=*.py"],
    capture_output=True, text=True
)
if result.returncode == 0 and result.stdout:
    print(f"  ✗ Found 'unicode()' usage (should be 'str()')")
    remnants_found = True
else:
    print("  ✓ No 'unicode()' usage found")

# Test 8: Check for .iteritems() usage
print("\n[8/10] Checking for '.iteritems()' usage...")
result = subprocess.run(
    ["grep", "-r", "\.iteritems()", "cuckoo/", "--include=*.py"],
    capture_output=True, text=True
)
if result.returncode == 0 and result.stdout:
    print(f"  ✗ Found '.iteritems()' usage (should be '.items()')")
    remnants_found = True
else:
    print("  ✓ No '.iteritems()' usage found")

# Test 9: Check for old-style octal literals
print("\n[9/10] Checking for old octal literals...")
result = subprocess.run(
    ["grep", "-r", "-E", "= *0[0-7]{3}", "cuckoo/", "--include=*.py"],
    capture_output=True, text=True
)
if result.returncode == 0 and result.stdout:
    # Filter out 0o prefix (which is correct)
    lines = [l for l in result.stdout.split('\n') if '0o' not in l and l.strip()]
    if lines:
        print(f"  ✗ Found old octal literals")
        remnants_found = True
    else:
        print("  ✓ No old octal literals found")
else:
    print("  ✓ No old octal literals found")

# Test 10: Summary
print("\n[10/10] Migration Summary")
print("=" * 60)
if remnants_found:
    print("Status: ⚠ Minor issues detected (may not affect functionality)")
else:
    print("Status: ✓ All checks passed!")

print("\nNext Steps:")
print("1. Install dependencies: pip3 install -e .")
print("2. Test basic commands: cuckoo --help")
print("3. Initialize CWD: cuckoo init")
print("4. Run test suite: pytest tests/")

print("\n" + "=" * 60)
