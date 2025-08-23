# CBIG Quick Command Reference

## 🚀 Most Common Commands

### Basic Analysis
```bash
# Analyze any directory
cbig main -p /path/to/project

# Current directory
cbig main -p .

# With documentation output
cbig main -p . --by-dir --output-dir docs/
```

### Performance Optimized
```bash
# Fast with caching
cbig main -p . --cache-dir .cbig_cache -j 8

# Language specific (faster)
cbig main -p . -l python
cbig main -p . -l javascript,typescript
```

### Output Formats
```bash
# JSON for tools/APIs
cbig main -p . --format json -o analysis.json --no-md

# YAML for readability
cbig main -p . --format yaml -o report.yaml

# Text summary to terminal
cbig main -p . --format txt
```

### Filtering
```bash
# Exclude common directories
cbig main -p . --exclude "node_modules/*" --exclude "build/*" --exclude ".git/*"

# Include specific patterns
cbig main -p . --include "src/**/*.py" --include "lib/**/*.js"
```

## 🎯 Aliases (After Setup)

```bash
cbig-here         # Current directory
cbig-docs         # Generate docs/
cbig-fast         # Cached + parallel
cbig-py           # Python only
cbig-js           # JavaScript only
cbig-ai .         # AI context file
cbig-summary .    # Quick summary
```

## 🔧 Installation

```bash
# Global CLI install
uv tool install --editable .

# Development install
uv sync

# Add aliases to shell
source ~/dv/tools/code-extractor/cbig/cbig_aliases.sh
```

## 📊 Exit Codes
- 0: Success
- 1: Invalid arguments
- 2: Parse error
- 3: I/O error
- 4: Unsupported language