# CBIG Commands PRD - Complete Terminal Input Reference
**Version:** 1.3.0  
**Last Updated:** 2025-01-22  
**Environment:** macOS (M3 Silicon) / Linux / Windows

---

## 🔧 ENVIRONMENT REQUIREMENTS

### Core Dependencies
- **Python:** 3.11+ (required)
- **UV Package Manager:** Latest version (required)
- **Shell:** zsh/bash/fish (autocomplete support varies)
- **Memory:** Minimum 2GB RAM available
- **Disk Space:** 500MB for cache operations

### Installation States
1. **Local Project Mode** - Running from project directory
2. **Global CLI Mode** - Installed via `uv tool install`
3. **Virtual Environment Mode** - Running within activated venv

---

## 📦 SECTION 1: INSTALLATION & SETUP COMMANDS

### 1.1 Initial Installation
```bash
uv tool install --editable /path/to/cbig
```
**Success Conditions:**
- ✅ UV package manager installed
- ✅ Python 3.11+ available
- ✅ Valid pyproject.toml present
- ✅ Write permissions to ~/.local/bin

**Failure Conditions:**
- ❌ UV not installed → Install with `curl -LsSf https://astral.sh/uv/install.sh | sh`
- ❌ Python < 3.11 → Upgrade Python first
- ❌ Missing pyproject.toml → Invalid CBIG installation
- ❌ Permission denied → Use sudo or fix permissions

### 1.2 Development Installation
```bash
cd /path/to/cbig
uv sync
```
**Success Conditions:**
- ✅ Current directory contains pyproject.toml
- ✅ Network access for package downloads
- ✅ No conflicting virtual environments

**Failure Conditions:**
- ❌ Wrong directory → Navigate to CBIG root
- ❌ Network timeout → Check internet connection
- ❌ VIRTUAL_ENV conflict → Run `deactivate` first

### 1.3 Dependency Update
```bash
uv sync --upgrade
```
**Success Conditions:**
- ✅ Valid pyproject.toml
- ✅ Network connectivity
- ✅ Compatible dependency versions available

**Failure Conditions:**
- ❌ Dependency conflicts → Review pyproject.toml constraints
- ❌ Breaking changes in updates → Pin specific versions

---

## 🚀 SECTION 2: BASIC EXECUTION COMMANDS

### 2.1 Standard Analysis
```bash
cbig main -p /path/to/project
```
**Success Conditions:**
- ✅ Path exists and is readable
- ✅ Contains supported source files
- ✅ Sufficient memory for analysis

**Failure Conditions:**
- ❌ Path not found → Verify path exists
- ❌ No source files → Check supported languages
- ❌ Permission denied → Fix read permissions
- ❌ Out of memory → Use --max-workers to limit parallelism

### 2.2 Current Directory Analysis
```bash
cbig main -p .
```
**Success Conditions:**
- ✅ Current directory contains code files
- ✅ Not in system directories (/, /usr, etc.)

**Failure Conditions:**
- ❌ Empty directory → No files to analyze
- ❌ Binary files only → CBIG analyzes source code only

### 2.3 With UV Run (Non-Global)
```bash
uv run cbig main -p /path/to/project
```
**Success Conditions:**
- ✅ In CBIG project directory
- ✅ Dependencies installed via `uv sync`
- ✅ UV environment active

**Failure Conditions:**
- ❌ Not in project root → Change to CBIG directory
- ❌ Dependencies missing → Run `uv sync` first

---

## 📊 SECTION 3: OUTPUT FORMAT COMMANDS

### 3.1 JSON Output
```bash
cbig main -p . --format json -o analysis.json --no-md
```
**Success Conditions:**
- ✅ Write permissions for output file
- ✅ Valid JSON serializable content
- ✅ Sufficient disk space

**Failure Conditions:**
- ❌ Write permission denied → Check directory permissions
- ❌ Disk full → Free up space
- ❌ Invalid characters in code → File encoding issues

### 3.2 YAML Output
```bash
cbig main -p . --format yaml -o report.yaml
```
**Success Conditions:**
- ✅ PyYAML installed
- ✅ Valid YAML-compatible data
- ✅ Output path writable

**Failure Conditions:**
- ❌ YAML serialization error → Complex objects in code
- ❌ File locked → Close other programs using file

### 3.3 Markdown Output (Default)
```bash
cbig main -p . --format md
```
**Success Conditions:**
- ✅ Jinja2 templates available
- ✅ Write permissions for markdown files

**Failure Conditions:**
- ❌ Template error → Corrupted installation
- ❌ Unicode errors → File encoding issues

### 3.4 Plain Text Summary
```bash
cbig main -p . --format txt
```
**Success Conditions:**
- ✅ Terminal supports text output
- ✅ Rich library installed for formatting

**Failure Conditions:**
- ❌ Terminal encoding issues → Set LANG=en_US.UTF-8

---

## 🗂️ SECTION 4: ORGANIZATION COMMANDS

### 4.1 Directory-Level Analysis
```bash
cbig main -p . --by-dir --output-dir docs/
```
**Success Conditions:**
- ✅ Output directory exists or can be created
- ✅ Sufficient disk space for multiple files
- ✅ Project has directory structure

**Failure Conditions:**
- ❌ Cannot create output-dir → Permission issue
- ❌ Single file input → Use --by-file instead
- ❌ Disk quota exceeded → Free up space

### 4.2 File-Level Analysis
```bash
cbig main -p src/main.py --by-file
```
**Success Conditions:**
- ✅ Target is a single file
- ✅ File is readable
- ✅ Supported file extension

**Failure Conditions:**
- ❌ Directory provided → Use --by-dir for directories
- ❌ Binary file → Not a source code file
- ❌ Unknown extension → Add to supported languages

### 4.3 Custom Template Output
```bash
cbig main -p . --md-template "{{dir}}_analysis_{{suffix}}.md"
```
**Success Conditions:**
- ✅ Valid Jinja2 template syntax
- ✅ Template variables exist (dir, suffix)

**Failure Conditions:**
- ❌ Invalid template syntax → Check Jinja2 documentation
- ❌ Undefined variables → Use only dir, suffix, timestamp

---

## ⚡ SECTION 5: PERFORMANCE OPTIMIZATION COMMANDS

### 5.1 Cached Analysis
```bash
cbig main -p . --cache-dir .cbig_cache
```
**Success Conditions:**
- ✅ Write permissions for cache directory
- ✅ Sufficient disk space (can be 10x source size)
- ✅ Consistent file system

**Failure Conditions:**
- ❌ Cache corruption → Use --clear-cache
- ❌ Disk full → Clear cache or increase space
- ❌ Network drive → Cache on local disk only

### 5.2 Parallel Processing
```bash
cbig main -p . -j 8
```
**Success Conditions:**
- ✅ System has 8+ CPU cores
- ✅ Sufficient RAM (500MB per worker)
- ✅ Files can be processed independently

**Failure Conditions:**
- ❌ Out of memory → Reduce worker count
- ❌ CPU throttling → System overheating
- ❌ File locks → Some files may be in use

### 5.3 Clear Cache
```bash
cbig main -p . --cache-dir .cbig_cache --clear-cache
```
**Success Conditions:**
- ✅ Cache directory exists
- ✅ Write permissions to delete cache

**Failure Conditions:**
- ❌ Cache in use → Stop other CBIG processes
- ❌ Permission denied → Check ownership

---

## 🔍 SECTION 6: FILTERING COMMANDS

### 6.1 Language Filtering
```bash
cbig main -p . -l python,javascript,rust
```
**Success Conditions:**
- ✅ Specified languages have parsers installed
- ✅ Project contains files of those languages
- ✅ Language names are valid

**Failure Conditions:**
- ❌ Unknown language → Check supported languages list
- ❌ No matching files → Verify file extensions
- ❌ Parser not installed → Missing tree-sitter parser

### 6.2 Include Patterns
```bash
cbig main -p . --include "src/**/*.py" --include "lib/**/*.js"
```
**Success Conditions:**
- ✅ Valid glob patterns
- ✅ Patterns match existing files
- ✅ Pathspec library available

**Failure Conditions:**
- ❌ Invalid glob syntax → Check glob documentation
- ❌ No matches → Verify file paths
- ❌ Too broad pattern → May cause memory issues

### 6.3 Exclude Patterns
```bash
cbig main -p . --exclude "tests/*" --exclude "node_modules/*" --exclude "*.min.js"
```
**Success Conditions:**
- ✅ Valid glob patterns
- ✅ Leaves some files to analyze

**Failure Conditions:**
- ❌ Excludes everything → Too broad patterns
- ❌ Pattern syntax error → Escape special characters

---

## 📋 SECTION 7: CONTENT CONTROL COMMANDS

### 7.1 Selective Sections
```bash
cbig main -p . --no-functions --no-classes --deps
```
**Success Conditions:**
- ✅ At least one section enabled
- ✅ Selected sections have data

**Failure Conditions:**
- ❌ All sections disabled → No output generated
- ❌ Language doesn't support section → E.g., no classes in C

### 7.2 Include Comments
```bash
cbig main -p . --comments
```
**Success Conditions:**
- ✅ Parser supports comment extraction
- ✅ Files contain comments

**Failure Conditions:**
- ❌ Parser limitation → Fallback to regex
- ❌ Minified code → No comments preserved

### 7.3 Sorting Options
```bash
cbig main -p . --sort functions=name --sort classes=size
```
**Success Conditions:**
- ✅ Valid sort fields (name, size, line)
- ✅ Sections contain sortable data

**Failure Conditions:**
- ❌ Invalid sort field → Check documentation
- ❌ Empty sections → Nothing to sort

---

## 🛠️ SECTION 8: DEBUGGING COMMANDS

### 8.1 Verbose Mode
```bash
cbig main -p . -v
```
**Success Conditions:**
- ✅ Terminal supports colored output
- ✅ Stderr is not redirected

**Failure Conditions:**
- ❌ Output too verbose → Use --quiet instead
- ❌ Terminal buffer overflow → Increase buffer size

### 8.2 Quiet Mode
```bash
cbig main -p . -q
```
**Success Conditions:**
- ✅ Only errors displayed
- ✅ Suitable for automation

**Failure Conditions:**
- ❌ Silent failures → Use verbose for debugging

### 8.3 Help Display
```bash
cbig main --help
```
**Success Conditions:**
- ✅ Terminal displays help text
- ✅ Typer CLI framework functional

**Failure Conditions:**
- ❌ Never fails unless installation corrupted

---

## 🎯 SECTION 9: ALIAS COMMANDS (After Setup)

### 9.1 Quick Analysis Aliases
```bash
cbig-here              # Analyze current directory
cbig-docs              # Generate docs/ folder
cbig-fast              # Cached + 8 workers
cbig-json              # JSON output
cbig-yaml              # YAML output
```
**Success Conditions:**
- ✅ Aliases sourced in ~/.zshrc or ~/.bashrc
- ✅ CBIG globally installed
- ✅ Current directory has code

**Failure Conditions:**
- ❌ Alias not found → Run `source ~/.zshrc`
- ❌ CBIG not in PATH → Reinstall with `uv tool install`

### 9.2 Language-Specific Aliases
```bash
cbig-py                # Python only
cbig-js                # JavaScript/TypeScript
cbig-web               # JS/TS/HTML/CSS
cbig-java              # Java only
cbig-rust              # Rust only
```
**Success Conditions:**
- ✅ Project contains specified language files
- ✅ Language parsers installed

**Failure Conditions:**
- ❌ No matching files → Wrong language selected
- ❌ Parser errors → Update tree-sitter parsers

### 9.3 Function Commands
```bash
cbig-analyze /path/to/project [output_dir]
cbig-file main.py
cbig-ai . context.md
cbig-summary /path
```
**Success Conditions:**
- ✅ Functions loaded in shell
- ✅ Valid paths provided
- ✅ Write permissions for output

**Failure Conditions:**
- ❌ Function not found → Source aliases file
- ❌ Invalid arguments → Check function signature
- ❌ Path errors → Verify paths exist

---

## 🔄 SECTION 10: PIPELINE & AUTOMATION COMMANDS

### 10.1 CI/CD Integration
```bash
cbig main -p . --format json -o metrics.json --no-md --quiet
```
**Success Conditions:**
- ✅ Exit code 0 on success
- ✅ Machine-readable output
- ✅ No interactive prompts

**Failure Conditions:**
- ❌ Non-zero exit codes → Check exit code meanings
- ❌ Parse errors → Exit code 2
- ❌ I/O errors → Exit code 3

### 10.2 Watch Mode (Custom Script)
```bash
while true; do
    cbig main -p . --cache-dir .cache
    sleep 60
done
```
**Success Conditions:**
- ✅ Cache speeds up repeated runs
- ✅ System resources available

**Failure Conditions:**
- ❌ Memory leak over time → Restart periodically
- ❌ Cache grows too large → Clear periodically

### 10.3 Batch Processing
```bash
for dir in */; do
    cbig main -p "$dir" -o "${dir%/}_analysis.md"
done
```
**Success Conditions:**
- ✅ Each directory is valid project
- ✅ Unique output names

**Failure Conditions:**
- ❌ Subdirectory errors → Add error handling
- ❌ Output overwrites → Check filenames

---

## 🚨 SECTION 11: ERROR RECOVERY COMMANDS

### 11.1 Force Reinstall
```bash
uv tool uninstall cbig
uv tool install --editable /path/to/cbig
```
**Success Conditions:**
- ✅ Clean uninstall completed
- ✅ Fresh installation successful

**Failure Conditions:**
- ❌ Tool in use → Close all CBIG processes
- ❌ Corrupted metadata → Delete ~/.local/share/uv manually

### 11.2 Reset Environment
```bash
rm -rf .cbig_cache
rm -rf .venv
rm -rf ~/.local/share/uv/tools/cbig
uv sync
```
**Success Conditions:**
- ✅ All caches cleared
- ✅ Fresh environment created

**Failure Conditions:**
- ❌ Permission issues → Use appropriate permissions
- ❌ Files in use → Stop all processes

### 11.3 Debug Tree-Sitter Issues
```bash
python -c "import tree_sitter_python; print('OK')"
```
**Success Conditions:**
- ✅ Parsers properly installed
- ✅ Binary compatibility

**Failure Conditions:**
- ❌ Module not found → Reinstall parser
- ❌ Binary mismatch → Wrong architecture

---

## 📊 EXIT CODES REFERENCE

| Code | Meaning | Resolution |
|------|---------|------------|
| 0 | Success | None needed |
| 1 | Invalid arguments | Check command syntax |
| 2 | Parse error | Check file encoding/format |
| 3 | I/O error | Check permissions/disk space |
| 4 | Unsupported language | Use supported languages |
| 127 | Command not found | Install CBIG properly |
| 137 | Out of memory | Reduce --max-workers |

---

## 🔐 PERMISSIONS MATRIX

| Operation | Required Permission | Check Command |
|-----------|-------------------|---------------|
| Read source | Read (r) | `ls -la /path` |
| Write output | Write (w) | `touch /path/test` |
| Create cache | Write + Execute (wx) | `mkdir -p /path/cache` |
| Install global | Write to ~/.local/bin | `ls -la ~/.local/bin` |

---

## ⚙️ ENVIRONMENT VARIABLES

### Optional Configuration
```bash
export CBIG_CACHE_DIR="$HOME/.cbig_cache"
export CBIG_MAX_WORKERS=4
export CBIG_DEFAULT_FORMAT="json"
export PYTHONPATH="/path/to/cbig/src:$PYTHONPATH"
```

### Debug Variables
```bash
export CBIG_DEBUG=1              # Enable debug logging
export CBIG_TRACE=1              # Enable trace logging
export PYTHONUNBUFFERED=1        # Immediate output
```

---

## 📝 NOTES

1. **Performance:** First run is always slower due to AST parsing
2. **Caching:** Cache can grow to 10x source size
3. **Memory:** Each worker uses ~500MB RAM
4. **Network:** Not required except for installation
5. **Compatibility:** M3 Silicon optimized, works on all platforms

---

**END OF PRD**