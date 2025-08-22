# CBIG - CodeBase Insight Generator

**Version 1.3.0** | Cross-language CLI extractor for directory-level code analysis

CBIG is a single-binary tool that walks any repository and produces Repomix-style markdown files and machine-readable reports. It provides directory-level summaries of libraries, functions, and classes with drill-down capabilities to individual files.

## Key Features

- **Directory-First View**: Complete overviews of what each directory provides
- **Multi-Language Support**: Python, Java, JavaScript/TypeScript, HTML, Rust, Swift
- **Flexible Output**: Markdown (Repomix-style), JSON, YAML, or plain text
- **Intelligent Caching**: Skip unchanged files on subsequent runs
- **Concurrent Processing**: Fast analysis with parallel workers
- **Native Performance**: Built with uv for Apple M3 silicon optimization

## Quick Start

### Installation

```bash
Install with uv (recommended)
uv tool install cbig
```

Or install locally

```bash

git clone <repo-url>
cd cbig
uv sync
uv run cbig --help

```


### Basic Usage

```bash
# Repository-wide analysis
cbig main -p ./myrepo
```

```bash
# Per-directory markdown files
cbig main -p . --by-dir --output-dir docs/

```
````bash
# Single file analysis  
cbig main -p src/user.py --by-file

````

```bash
# Structured output only
cbig main -p . --format yaml -o report.yaml --no-md

```

```bash
# With caching for faster subsequent runs
cbig main -p . --cache-dir .cbig_cache
```
## Command Reference

### Main Options

| Flag | Description | Example |
|------|-------------|---------|
| `--path -p` | Root path to analyze | `-p ./repo` |
| `--language -l` | Filter by languages | `-l python,java` |
| `--by-dir` | Generate per-directory markdown | `--by-dir` |
| `--by-file` | Generate per-file markdown | `--by-file` |
| `--format -f` | Output format (json/yaml/md/txt) | `-f yaml` |
| `--output-dir` | Directory for markdown files | `--output-dir docs/` |
| `--cache-dir` | Enable caching | `--cache-dir .cache` |

### Section Control

| Flag | Description |
|------|-------------|
| `--deps/--no-deps` | Include/exclude dependencies |
| `--functions/--no-functions` | Include/exclude functions |
| `--classes/--no-classes` | Include/exclude classes |
| `--comments/--no-comments` | Include/exclude comments |

### Advanced Options

| Flag | Description |
|------|-------------|
| `--sort` | Sort sections (e.g., `functions=name`) |
| `--max-workers -j` | Parallel workers (default: CPU count) |
| `--md-template` | Custom filename template |
| `--include/--exclude` | File pattern filters |

## Output Examples

### Repository Overview

# MyRepo | Repository Overview

##  Summary
- **Total Files**: 245
- **Total Lines of Code**: 12,450
- **Languages**: python, javascript

## Libraries / Imports
| Library / Package | Version | Source | Language |
|-------------------|---------|---------|----------|
| requests | 2.31.0 | pip | python |
| react | 18.2.0 | npm | javascript |

## Functions / Methods
| Name | Signature | Lines | File | Docstring |
|------|-----------|-------|------|-----------|
| process_data | `def process_data(input: str) dict` | 42-58 | utils.py | Parse and validate... |

## Classes / Types  
| Name | Kind | Inherits / Implements | Lines | File | Doc |
|------|------|-----------------------|-------|------|-----|
| UserService | class | BaseService (extends) | 12-210| user.py | Service layer... |

### Structured Output (JSON)

```json
{
  "repo": {
    "root": "/path/to/repo",
    "languages": ["python", "javascript"],
    "summary": {
      "total_files": 245,
      "total_loc": 12450,
      "per_language": {
        "python": {"files": 120, "loc": 8000},
        "javascript": {"files": 125, "loc": 4450}
      }
    }
  },
  "dependencies": [...],
  "functions": [...],
  "classes": [...]
}
```

## Use Cases

### For Developers
- **Quick Repository Overview**: Understand any codebase structure instantly
- **Dependency Auditing**: See all external libraries at a glance  
- **Code Architecture**: Visualize class hierarchies and function organization

### For Tech Leads
- **Code Reviews**: Review directory-level changes efficiently
- **Architecture Decisions**: Enforce language and dependency policies
- **Documentation**: Auto-generate architectural overviews

### For CI/CD
- **Automated Checks**: Validate dependency changes
- **Security Scanning**: Extract dependency lists for vulnerability checks
- **Documentation**: Keep architecture docs up-to-date

## Advanced Features

### Caching for Performance

```bash
# First run - analyzes all files
cbig main -p . --cache-dir .cbig_cache

# Subsequent runs - only re-analyzes changed files  
cbig main -p . --cache-dir .cbig_cache

# Much faster!
```

### Custom Templates

```bash
# Custom filename pattern
cbig main -p . --by-dir --md-template "{{dir}}_analysis_{{suffix}}.md"
# Generates: api_analysis_p.md, web_analysis_j.md, etc.
```

### Language Filtering

```bash
# Analyze only Python and Rust files
cbig main -p . -l python,rust

# Exclude test directories
cbig main -p . --exclude "tests/*" --exclude "**/*_test.py"
```

## Architecture

CBIG follows a modular architecture:

```

