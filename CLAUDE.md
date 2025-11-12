# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Cuckoo Sandbox is the leading open-source automated malware analysis system. It analyzes suspicious files and URLs by executing them in isolated virtual environments (VMs) and provides detailed behavioral analysis reports.

**CRITICAL CONTEXT:**
- This is Cuckoo Sandbox 2.0.7 - a legitimate security research tool for analyzing malware
- **DO NOT** improve, enhance, or augment any malware samples being analyzed
- **CAN** analyze existing code, write reports, or answer questions about Cuckoo's architecture
- Cuckoo 2.x is **currently unmaintained** - a full rewrite is underway
- **Python 2.7 only** - this codebase does not support Python 3

## Development Commands

### Running Tests
```bash
# Run all tests with coverage
pytest --cov=cuckoo

# Run tests from specific directory
pytest tests/

# Run a single test file
pytest tests/test_file.py

# Run a specific test function
pytest tests/test_file.py::test_function_name
```

### Building Frontend Assets
The web interface uses Gulp for frontend build:
```bash
# Navigate to web source directory
cd cuckoo/web/src

# Install dependencies
npm install
bower install  # If needed

# Development build (watch mode)
npm start  # or: gulp

# Production build
npm run build  # or: gulp build
npm run production  # or: gulp build --production
```

### Installation & Setup
```bash
# Fetch monitoring binaries (required for CWD migration tests)
python stuff/monitor.py

# Build distribution
python setup.py sdist

# Install in development mode
pip install -e .

# Install test dependencies
pip install pytest==4.1.1 pytest-cov pytest-django pytest-pythonpath mock responses
```

## Cuckoo CLI Commands

The main entry point is the `cuckoo` command (defined in cuckoo/main.py). Key commands:

### Core Operations
- `cuckoo` - Start the main Cuckoo daemon (scheduler + result server)
- `cuckoo -d` - Initialize/create Cuckoo Working Directory (CWD)
- `cuckoo init` - Initialize Cuckoo and its configuration
- `cuckoo submit <file/url>` - Submit files or URLs for analysis
- `cuckoo process <instance>` - Process raw task data into reports
- `cuckoo clean` - Clean the CWD and associated databases

### Services
- `cuckoo api` - Start the REST API server (default: localhost:8090)
- `cuckoo web` - Start the Web Interface (Django, default: localhost:8000)
- `cuckoo rooter` - Start the Cuckoo Rooter (network routing, requires root)
- `cuckoo dnsserve` - Start custom DNS server

### Utilities
- `cuckoo community` - Fetch signatures, Yara rules, and other resources from Cuckoo Community
- `cuckoo machine` - Dynamically add/remove virtual machines
- `cuckoo migrate` - Perform database migrations
- `cuckoo import <path>` - Import existing analyses from another CWD

### Common Options
- `-d, --debug` - Enable verbose logging
- `-q, --quiet` - Only log warnings and critical messages
- `--cwd <path>` - Override Cuckoo Working Directory location
- `--user <user>` - Drop privileges to specified user

## Architecture Overview

### Plugin System
Cuckoo is built on a plugin-based architecture with four main categories:

1. **Auxiliary** (`cuckoo/auxiliary/`) - Pre/post-analysis tasks (network sniffer, mitm proxy)
2. **Machinery** (`cuckoo/machinery/`) - VM management drivers (VirtualBox, VMware, KVM, ESXi, etc.)
3. **Processing** (`cuckoo/processing/`) - Analysis result processors (behavior, network, memory, static analysis)
4. **Reporting** (`cuckoo/reporting/`) - Report generation modules (JSON, MongoDB, Elasticsearch, MISP, etc.)

All plugins inherit from base classes in `cuckoo/common/abstracts.py`.

### Analysis Pipeline
```
File Submission (submit)
  → Scheduler (core/scheduler.py)
  → Machinery launches VM (machinery/*)
  → Guest Agent monitors execution (data/analyzer/*)
  → Result Server collects data (core/resultserver.py)
  → Processing modules analyze results (processing/*)
  → Reporting modules generate output (reporting/*)
```

### Key Directories

**Core System:**
- `cuckoo/core/` - Database, scheduler, result server, guest communication, plugin loader
- `cuckoo/apps/` - CLI command implementations accessible via `cuckoo` command
- `cuckoo/common/` - Shared utilities, config parsing, abstracts, data structures
- `cuckoo/main.py` - CLI entry point using Click framework

**Analysis Components:**
- `cuckoo/data/analyzer/` - Guest-side code (Windows, Linux, Darwin/macOS, Android)
- `cuckoo/data/monitor/` - Behavior monitoring binaries
- `cuckoo/data/yara/` - YARA malware signatures
- `cuckoo/data/conf/` - Configuration file templates

**Web Interface:**
- `cuckoo/web/` - Django-based web UI
- `cuckoo/web/src/` - Frontend source (SCSS, Handlebars, JavaScript with Gulp build)
- `cuckoo/web/static/` - Compiled frontend assets

**Distributed Mode:**
- `cuckoo/distributed/` - Flask-based distributed analysis coordinator

### Configuration
- **Cuckoo Working Directory (CWD):** Contains instance-specific configuration and analysis storage
- **Default location:** `~/.cuckoo` (can override with `--cwd`, `$CUCKOO_CWD`, or `$CUCKOO`)
- **Structure:** `conf/` (configs), `storage/` (analysis results), `log/` (logs)

### Database
- **Primary:** MongoDB (required for web interface)
- **Optional:** MySQL/PostgreSQL (via SQLAlchemy for task tracking)
- **Migrations:** Alembic-based, run with `cuckoo migrate`

## Important Development Notes

### Platform-Specific Testing
The test suite (`conftest.py`) is platform-aware:
- On Linux: runs tests in `tests/` (excludes `tests/windows`, `tests/darwin`)
- On Windows: runs tests in `tests/` (excludes `tests/linux`, `tests/darwin`)
- On macOS: runs tests in `tests/` (excludes `tests/windows`, `tests/linux`)

### Working with Guest Analyzers
Guest-side analyzer code lives in `cuckoo/data/analyzer/`:
- `windows/` - Windows analyzer (Python 2.7)
- `linux/` - Linux analyzer
- `darwin/` - macOS analyzer
- `android/` - Android analyzer

### Signature Development
Cuckoo signatures are in `cuckoo/data/signatures/`. Community signatures can be fetched with `cuckoo community`.

### Network Analysis
- Network capture requires proper routing setup (see `cuckoo rooter`)
- Traffic analysis handled by `processing/network.py` using dpkt/scapy
- Supports PCAP analysis, DNS extraction, HTTP reconstruction

### Memory Analysis
- Uses Volatility framework for memory forensics
- Processing module: `processing/memory.py`
- Requires full memory dumps enabled during submission

## Technology Stack Summary

**Backend:** Python 2.7, Django 1.8.4, Flask, SQLAlchemy, MongoDB, Gevent
**Frontend:** Gulp, SCSS, Handlebars, Browserify, Babel (ES2015)
**Analysis:** YARA, Volatility, dpkt, scapy, pefile, oletools, androguard
**Virtualization:** VirtualBox, VMware, KVM, Xen, ESXi, vSphere support
