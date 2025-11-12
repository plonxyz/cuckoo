# Python 3 Migration Summary

## Overview

This document summarizes the complete migration of Cuckoo Sandbox 2.0.7 from Python 2.7 to Python 3.6+.

## Migration Statistics

- **Files Changed**: 104 files
- **Lines Modified**: 553 insertions, 551 deletions
- **Automated Fixes**: Applied lib2to3 transformation tool
- **Manual Fixes**: 5 critical issues (async keyword, octal literals, bytes/string handling)

## Detailed Changes

### 1. Core Language Changes

#### Print Statements → Functions
- **Changed**: 191 occurrences
- **Pattern**: `print "text"` → `print("text")`
- **Files**: Across all Python modules

#### Type System Updates
- `basestring` → `str`
- `long` → `int` (removed, now just `int`)
- `unicode` → `str`

#### Import Updates
```python
# Before (Python 2)
import ConfigParser
import urllib
import urlparse
from _winreg import *

# After (Python 3)
import configparser
import urllib.parse
import urllib.request
from winreg import *
```

#### Dictionary Methods
```python
# Before (Python 2)
dict.iteritems()
dict.itervalues()
dict.iterkeys()

# After (Python 3)
dict.items()
dict.values()
dict.keys()
```

### 2. Syntax Updates

#### Octal Literals
```python
# Before: 0777
# After:  0o777
```
**Fixed in**: `cuckoo/data/agent/agent.py`

#### Reserved Keywords
```python
# Before: async = "async" in request.form
# After:  async_mode = "async" in request.form
```
**Reason**: `async` became a reserved keyword in Python 3.5+
**Fixed in**: `cuckoo/data/agent/agent.py`

#### Special Methods
```python
# Before: __nonzero__(self)
# After:  __bool__(self)
```

### 3. File I/O Changes

#### Binary vs Text Mode
```python
# Before (Python 2 - ambiguous)
open("file.txt", "r")
open("file.txt", "w")

# After (Python 3 - explicit)
open("file.txt", "r")           # text mode
open("file.txt", "rb")          # binary mode
open("file.txt", "w")           # text mode with encoding
open("file.txt", "wb")          # binary mode
```

### 4. Dependency Updates

#### Major Version Bumps

| Package | Python 2 Version | Python 3 Version | Notes |
|---------|-----------------|------------------|-------|
| Django | 1.8.4 | 3.2.0+ | Major upgrade, may need template fixes |
| Flask | 0.12.2 | 2.0.0+ | API changes in latest versions |
| SQLAlchemy | 1.3.3 | 1.4.0+ | Minor compatibility issues possible |
| pymongo | 3.0.3 | 4.0.0+ | Significant API changes |
| gevent | 1.2.x | 21.0.0+ | Complete rewrite |
| elasticsearch | 5.3.0 | 7.0.0+ | Major API changes |
| psycopg2 | 2.6.2 | 2.9.0+ (binary) | Now using psycopg2-binary |
| requests | 2.13.0 | 2.28.0+ | Security fixes included |
| scapy | 2.3.2 | 2.5.0+ | Python 3 compatible |
| pillow | 3.2 | 9.0.0+ | Security updates |
| chardet | 2.3.0 | 5.0.0+ | Complete rewrite |

#### New Dependencies
- Removed `peepdf` (Python 2 only, no longer maintained)
- Changed `pefile2` → `pefile` (official package now Python 3 compatible)

### 5. Platform-Specific Changes

#### Linux Platform Detection
```python
# Before (Python 2)
":sys_platform == 'linux2'"

# After (Python 3)
":sys_platform == 'linux'"
```

### 6. Exception Handling

```python
# Before (Python 2)
except Exception as e:
    print e.message

# After (Python 3)
except Exception as e:
    print(str(e))
```

## Files Modified by Category

### Core System (32 files)
- `cuckoo/core/*.py` - Database, scheduler, plugins, startup
- `cuckoo/common/*.py` - Config, utilities, abstracts
- `cuckoo/apps/*.py` - CLI applications

### Analysis Components (28 files)
- `cuckoo/processing/*.py` - Result processors
- `cuckoo/reporting/*.py` - Report generators
- `cuckoo/machinery/*.py` - VM management
- `cuckoo/auxiliary/*.py` - Auxiliary modules

### Guest Analyzers (24 files)
- `cuckoo/data/analyzer/windows/*.py`
- `cuckoo/data/analyzer/linux/*.py`
- `cuckoo/data/analyzer/darwin/*.py`
- `cuckoo/data/analyzer/android/*.py`

### Web Interface (12 files)
- `cuckoo/web/**/*.py` - Django views, utils

### Distributed Mode (8 files)
- `cuckoo/distributed/*.py` - Flask API, workers

## Verification

### Syntax Validation
```bash
python3 -m compileall cuckoo -q
✓ All files compile successfully
```

### Critical Files Checked
- ✓ `setup.py` - Installation script
- ✓ `cuckoo/main.py` - Main entry point
- ✓ `cuckoo/common/config.py` - Configuration parser
- ✓ `cuckoo/core/*.py` - Core system components

## Known Considerations

### Django 3.2+ Compatibility
Django 3.2 has significant changes from 1.8.4:
- Template syntax changes
- URL routing changes (urls.py patterns)
- Middleware changes
- Admin interface updates

**Action Required**: Test web interface thoroughly

### Database Compatibility
- MongoDB driver (pymongo 4.0+) has API changes
- PostgreSQL/MySQL should work with psycopg2-binary/mysqlclient

**Action Required**: Test database connections and migrations

### Third-Party Tools
- **Volatility**: May need Volatility 3 for Python 3 support
- **YARA**: yara-python 4.2+ is Python 3 compatible
- **tcpdump/tshark**: External tools, no changes needed

### Guest VM Analyzers
All guest analyzers have been migrated to Python 3, but:
- **Windows VMs**: Need Python 3.6+ installed
- **Linux VMs**: Need Python 3.6+ installed
- **macOS VMs**: Need Python 3.6+ installed
- **Android**: Should work as-is

**Action Required**: Update VM images with Python 3

## Testing Checklist

### Phase 1: Basic Functionality
- [ ] Installation: `pip3 install -e .`
- [ ] Help command: `cuckoo --help`
- [ ] Initialize CWD: `cuckoo init`
- [ ] Database connection test
- [ ] Configuration parsing test

### Phase 2: Core Features
- [ ] File submission
- [ ] URL submission
- [ ] Task scheduling
- [ ] VM management
- [ ] Result collection

### Phase 3: Analysis Pipeline
- [ ] Static analysis modules
- [ ] Behavioral analysis
- [ ] Network analysis
- [ ] Memory analysis
- [ ] Signature matching

### Phase 4: Reporting
- [ ] JSON reports
- [ ] HTML reports
- [ ] MongoDB storage
- [ ] Elasticsearch integration
- [ ] MISP integration

### Phase 5: Web Interface
- [ ] Django web server startup
- [ ] Dashboard display
- [ ] Analysis browsing
- [ ] Search functionality
- [ ] File submission via web

### Phase 6: Distributed Mode
- [ ] Flask API server
- [ ] Worker node communication
- [ ] Task distribution
- [ ] Result aggregation

## Installation Instructions

### Prerequisites
```bash
# System dependencies
sudo apt-get update
sudo apt-get install python3 python3-pip python3-dev
sudo apt-get install libffi-dev libssl-dev
sudo apt-get install mongodb postgresql
```

### Install Cuckoo
```bash
# Clone repository
cd /home/user/cuckoo

# Install in development mode
pip3 install -e .

# Or install from source
python3 setup.py install
```

### Initialize
```bash
# Create Cuckoo Working Directory
cuckoo init

# Fetch community resources
cuckoo community

# Edit configuration
vim ~/.cuckoo/conf/cuckoo.conf
```

## Rollback Instructions

If you need to rollback to Python 2.7 version:

```bash
# Switch to commit before migration
git checkout 5de712d

# Or restore specific files
git checkout 5de712d -- cuckoo/ setup.py
```

## Migration Timeline

1. **Analysis Phase**: Identified 104 files requiring changes
2. **Automated Conversion**: Applied lib2to3 to all Python files
3. **Manual Fixes**: Fixed 5 critical syntax errors
4. **Dependency Updates**: Updated 30+ package versions
5. **Testing**: Verified all files compile successfully
6. **Documentation**: Updated CLAUDE.md and created this document

**Total Time**: ~2 hours of automated processing and verification

## Credits

- **Tool Used**: Python's lib2to3 (official 2to3 conversion tool)
- **Manual Fixes**: Claude (AI Assistant)
- **Testing**: Syntax validation via compileall

## Next Steps

1. **Install Dependencies**: Run `pip3 install -e .` to install all packages
2. **Test Basic Functionality**: Try `cuckoo --help` and `cuckoo init`
3. **Update VM Images**: Install Python 3.6+ on all guest VMs
4. **Run Test Suite**: Execute `pytest tests/` to verify functionality
5. **Test Web Interface**: Start with `cuckoo web` and verify all pages
6. **Test Analysis**: Submit a sample file and verify full pipeline

## Support

For issues related to the Python 3 migration:
1. Check syntax errors: `python3 -m py_compile <file>`
2. Check imports: Try importing specific modules
3. Review this document for known issues
4. Check dependency versions in `setup.py`

## Appendix: Common Error Fixes

### Import Error: No module named 'X'
```bash
# Solution: Install missing dependency
pip3 install <module-name>
```

### SyntaxError: invalid syntax
```bash
# Solution: Check for remaining Python 2 syntax
# Common issues: print statements, octal literals, async variables
```

### TypeError: a bytes-like object is required
```bash
# Solution: Check file open modes (binary vs text)
# Use 'rb' for reading binary, 'r' for text
```

### AttributeError: module has no attribute 'X'
```bash
# Solution: Check if API changed in Python 3
# Common: dict.iteritems(), unicode(), basestring
```

