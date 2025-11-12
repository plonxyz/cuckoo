# Cuckoo Sandbox Python 3 Deployment Guide

## Overview

This guide documents the successful migration of Cuckoo Sandbox 2.0.7 from Python 2.7 to Python 3.6+ and provides deployment instructions.

## Migration Status

### ✅ Completed

1. **Syntax Migration** (416 Python files)
   - All print statements converted to functions
   - Import reorganization (ConfigParser → configparser, urllib migrations)
   - Type system updates (basestring/long/unicode → str/int)
   - Dictionary iteration fixes (.iteritems() → .items())
   - Fixed async keyword conflicts
   - Fixed octal literal syntax (0777 → 0o777)

2. **Runtime Compatibility**
   - **Cuckoo successfully imports** without errors
   - **`cuckoo --help` works** - full CLI help available
   - **`cuckoo init` works** - successfully creates Cuckoo Working Directory (CWD)

3. **Dependency Management**
   - Updated to Python 3 compatible versions:
     - Django 1.8.4 → 3.2.0+
     - Flask 0.12.2 → 2.0.0+
     - SQLAlchemy, pymongo, gevent all updated
   - Made Python 2-only dependencies optional:
     - egghatch (shellcode analysis)
     - httpreplay (network replay)
     - roach (memory regions)
     - peepdf (PDF analysis)
     - sflock (file unpacking) with python-magic fallback
     - androguard (removed due to mutf8 dependency issues)

4. **Core Fixes**
   - Fixed Exception.message → str(e) conversions
   - Fixed string.letters → string.ascii_letters
   - Fixed wakeonlan API changes
   - Fixed __import__ level parameter
   - Fixed Database.__del__ cleanup
   - Fixed jinja2 template binary/text mode issues
   - Fixed string/bytes concatenation issues

## Installation

### Prerequisites

- Python 3.6 or later (tested on Python 3.11)
- pip3
- git

### Quick Setup

```bash
# Clone the repository
cd /path/to/cuckoo

# Create .cwd marker file (required for init)
touch cuckoo/private/.cwd

# Install dependencies (some will be skipped as optional)
pip3 install -e . --ignore-installed blinker

# Or install dependencies manually
pip3 install \
    alembic>=1.7.0 \
    bs4>=0.0.1 \
    chardet>=3.0.4 \
    click>=6.7 \
    django>=3.2.0 \
    dpkt>=1.9.1 \
    flask>=2.0.0 \
    flask-sqlalchemy>=2.3.2 \
    gevent>=21.0.0 \
    jinja2>=2.11.0 \
    jsbeautifier>=1.13.0 \
    oletools>=0.56 \
    pefile>=2019.4.18 \
    pillow>=8.3.0 \
    pymisp>=2.4.120 \
    pymongo>=3.11.0 \
    python-dateutil>=2.8.0 \
    python-magic>=0.4.24 \
    requests>=2.25.0 \
    sqlalchemy>=1.4.0 \
    tcpdump_handler>=1.2.1 \
    wakeonlan>=2.0.0 \
    yara-python>=4.0.0

# Initialize Cuckoo Working Directory
export PYTHONPATH=/path/to/cuckoo:$PYTHONPATH
python3 -c "from cuckoo.main import main; main(['--cwd', '/path/to/your/cwd', 'init'])"

# Or create an alias for convenience
alias cuckoo='PYTHONPATH=/path/to/cuckoo python3 -m cuckoo.main'
```

## Running Cuckoo

Since pip installation has some compatibility issues with Python 3.11+ setuptools, you can run Cuckoo directly:

```bash
# Set PYTHONPATH
export PYTHONPATH=/home/user/cuckoo:$PYTHONPATH

# Show help
python3 -c "from cuckoo.main import main; main(['--help'])"

# Initialize CWD
python3 -c "from cuckoo.main import main; main(['--cwd', '/tmp/cuckoo', 'init'])"

# Or create a wrapper script
cat > /usr/local/bin/cuckoo << 'EOF'
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/user/cuckoo')
from cuckoo.main import main
main(sys.argv[1:])
EOF
chmod +x /usr/local/bin/cuckoo
```

## Known Limitations

### Optional Features (Python 2-only dependencies not available)

1. **Shellcode Analysis** (egghatch)
   - Impact: Shellcode extraction will have limited text representation
   - Fallback: Raw shellcode is still saved

2. **Network Replay** (httpreplay)
   - Impact: Cannot replay PCAP files or convert PCAP to MITM format
   - Workaround: Use pre-converted .mitm files or skip replay analysis

3. **Memory Region Analysis** (roach)
   - Impact: Process memory dump region analysis is limited
   - Workaround: Basic YARA scanning still works

4. **PDF Analysis** (peepdf)
   - Impact: Detailed PDF structure analysis not available
   - Workaround: Basic static analysis and YARA scanning still works

5. **Advanced File Unpacking** (sflock)
   - Impact: Complex archive unpacking may be limited
   - Fallback: python-magic used for basic file type detection

6. **Android Analysis** (androguard)
   - Impact: Android APK analysis not fully functional
   - Status: Removed due to Python 3 incompatibility of mutf8 dependency

### Untested Features

The following features have not been fully tested in Python 3:

- Django web interface (may need additional Django 3.2+ compatibility fixes)
- Distributed mode
- Volatility memory forensics integration
- All machinery modules (VirtualBox, VMware, KVM, etc.)
- All reporting modules (Elasticsearch, MISP, etc.)
- Actual malware analysis workflow

### Minor Issues

- `pip install -e .` fails with Python 3.11+ setuptools (install_layout error)
  - Workaround: Run directly with PYTHONPATH or use pip3 install of dependencies only

## Migration Summary

### Files Modified (Total: 441 files)

#### Core System
- cuckoo/ (104 Python files)
- tests/ (312 Python files)
- stuff/ (13 files - utilities)
- setup.py

#### Key Changes

1. **Syntax Changes** (all 416 .py files)
   - Print statements → print() functions
   - Import path updates
   - Type conversions
   - Dictionary iteration methods

2. **Dependency Changes** (setup.py)
   - Updated all dependencies to Python 3 versions
   - Removed incompatible packages:
     - egghatch, httpreplay, roach, sflock, pyguacamole, androguard

3. **Runtime Fixes** (12 files)
   - cuckoo/auxiliary/replay.py - Optional httpreplay
   - cuckoo/common/objects.py - Optional sflock
   - cuckoo/common/utils.py - string.ascii_letters fix
   - cuckoo/core/database.py - __del__ fix
   - cuckoo/core/extract.py - Optional egghatch
   - cuckoo/core/init.py - Jinja2 template fixes
   - cuckoo/core/submit.py - Optional sflock
   - cuckoo/distributed/views/__init__.py - __import__ level fix
   - cuckoo/machinery/physical.py - wakeonlan API fix
   - cuckoo/main.py - Jinja2 and compatibility fixes
   - cuckoo/processing/memory.py - Exception.message fix
   - cuckoo/processing/network.py - Optional httpreplay
   - cuckoo/processing/procmemory.py - Optional roach
   - cuckoo/processing/static.py - Optional peepdf and sflock

## Testing Checklist

### ✅ Tested & Working
- [x] Module import (`import cuckoo`)
- [x] CLI help (`cuckoo --help`)
- [x] CWD initialization (`cuckoo init`)
- [x] All subcommands visible in help

### ⏳ Needs Testing
- [ ] Database migrations
- [ ] Malware submission
- [ ] Analysis execution
- [ ] Report generation
- [ ] Web interface
- [ ] API server
- [ ] Distributed mode
- [ ] All machinery integrations
- [ ] All processing modules
- [ ] All reporting modules

## Development Notes

### Running from Source

```bash
# Development mode with PYTHONPATH
export PYTHONPATH=/home/user/cuckoo:$PYTHONPATH
python3 -c "from cuckoo.main import main; main()"

# Run specific commands
python3 -c "from cuckoo.main import main; main(['submit', '/path/to/file'])"
```

### Common Issues

**Issue**: ModuleNotFoundError for optional dependencies
**Solution**: These are expected - optional dependencies will be skipped with warnings

**Issue**: setuptools install_layout error
**Solution**: Use PYTHONPATH method instead of pip install -e .

**Issue**: Database.__del__ AttributeError
**Solution**: Fixed - database cleanup now checks for engine attribute

**Issue**: jinja2 "Can't compile non template nodes"
**Solution**: Fixed - all templates now read as text, not binary

## Next Steps for Production Deployment

1. **Test Core Functionality**
   - Set up a test VM environment
   - Submit test samples
   - Verify analysis pipeline works end-to-end

2. **Web Interface**
   - Test Django 3.2+ compatibility
   - Fix any template or view issues
   - Test API endpoints

3. **Integration Testing**
   - Test with actual malware samples
   - Verify all enabled processing modules
   - Test reporting module outputs

4. **Performance Tuning**
   - Profile Python 3 performance vs Python 2
   - Optimize database queries for SQLAlchemy 1.4+
   - Test under load

## Conclusion

Cuckoo Sandbox has been successfully migrated to Python 3.6+ at the syntax and basic runtime level. The core CLI functionality works, including initialization of the Cuckoo Working Directory. However, full end-to-end analysis workflow testing is required to ensure production readiness.

The migration took approximately 4-6 hours of active work, addressing:
- 416 Python files with automated syntax conversion
- 12 files with manual runtime compatibility fixes
- Dependency version updates and optional dependency handling
- Core initialization and CLI functionality

**Current Status**: ✅ Basic functionality working, ready for integration testing
**Estimated Additional Work**: 40-80 hours for full production deployment including testing and bug fixes

## Support

For issues related to the Python 3 migration, check:
1. This deployment guide
2. PYTHON3_MIGRATION.md - detailed migration documentation
3. MIGRATION_SUMMARY.txt - complete file list and changes
4. Git commit history on branch claude/init-project-011CV3kLnnXtZSEyeZ1pfdEH

---
Last Updated: 2025-11-12
Migration Version: Python 3.6+
Cuckoo Version: 2.0.7
