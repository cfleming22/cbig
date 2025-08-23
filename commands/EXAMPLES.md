# CBIG Command Examples - Real World Usage

## 🎯 PROJECT-SPECIFIC EXAMPLES

### Python Django Project
```bash
# Full analysis with caching
cbig main -p ~/my_django_project \
  --cache-dir .cbig_cache \
  -l python \
  --exclude "migrations/*" \
  --exclude "static/*" \
  --exclude "media/*" \
  --by-dir \
  --output-dir docs/architecture/

# Dependencies only
cbig main -p ~/my_django_project \
  -l python \
  --no-functions \
  --no-classes \
  --format yaml \
  -o requirements_analysis.yaml
```

### React/Next.js Project
```bash
# Full stack analysis
cbig main -p ~/my_nextjs_app \
  -l javascript,typescript \
  --exclude "node_modules/*" \
  --exclude ".next/*" \
  --exclude "out/*" \
  --by-dir \
  --output-dir docs/

# Component analysis
cbig main -p ~/my_nextjs_app/components \
  -l javascript,typescript \
  --functions \
  --classes \
  --format json \
  -o components_api.json
```

### Rust Project
```bash
# Cargo project analysis
cbig main -p ~/my_rust_project \
  -l rust \
  --exclude "target/*" \
  --exclude "Cargo.lock" \
  --by-dir \
  --cache-dir .cbig_cache

# Module structure only
cbig main -p ~/my_rust_project/src \
  -l rust \
  --no-deps \
  --sort functions=name \
  --sort classes=name
```

### Java Spring Boot
```bash
# Full project scan
cbig main -p ~/my_spring_app \
  -l java \
  --exclude "target/*" \
  --exclude ".mvn/*" \
  --exclude "*.class" \
  --by-dir \
  -j 8

# Service layer only
cbig main -p ~/my_spring_app/src/main/java/com/company/service \
  -l java \
  --classes \
  --functions \
  --comments
```

### Mixed Language Monorepo
```bash
# Analyze everything
cbig main -p ~/monorepo \
  --exclude "node_modules/*" \
  --exclude "**/build/*" \
  --exclude "**/dist/*" \
  --exclude "**/.git/*" \
  --by-dir \
  --output-dir docs/code-analysis/ \
  --cache-dir .cbig_cache \
  -j 8

# Backend only
cbig main -p ~/monorepo/backend \
  -l python,go \
  --by-dir

# Frontend only
cbig main -p ~/monorepo/frontend \
  -l javascript,typescript,css \
  --by-dir
```

## 📋 USE CASE EXAMPLES

### Generate AI Context File
```bash
# For Claude/ChatGPT context
cbig main -p . \
  --format md \
  --comments \
  --cache-dir .cbig_cache \
  -o ai_context.md

# Minimal context (functions only)
cbig main -p . \
  --no-deps \
  --no-classes \
  --functions \
  --format md \
  -o functions_only.md
```

### Code Review Preparation
```bash
# Generate review docs
cbig main -p feature_branch/ \
  --by-dir \
  --output-dir code_review/ \
  --comments \
  --sort functions=size \
  --sort classes=size

# Compare with main branch
cbig main -p main_branch/ -o main.json --format json --no-md
cbig main -p feature_branch/ -o feature.json --format json --no-md
```

### Documentation Generation
```bash
# Full documentation
cbig main -p . \
  --by-dir \
  --output-dir documentation/ \
  --comments \
  --md-template "{{dir}}_technical_doc.md"

# API documentation
cbig main -p src/api \
  --functions \
  --classes \
  --comments \
  --format md \
  -o API_REFERENCE.md
```

### CI/CD Integration
```bash
# Jenkins/GitHub Actions
cbig main -p . \
  --format json \
  -o build/code_metrics.json \
  --no-md \
  --quiet \
  --exclude "test/*" \
  -j 2

# With error checking
cbig main -p . --format json -o metrics.json --quiet || exit 1
```

### Security Audit Prep
```bash
# Find all dependencies
cbig main -p . \
  --deps \
  --no-functions \
  --no-classes \
  --format yaml \
  -o security/dependencies.yaml

# Identify entry points
cbig main -p . \
  --functions \
  --include "**/main.*" \
  --include "**/server.*" \
  --include "**/app.*"
```

## 🔄 BATCH PROCESSING EXAMPLES

### Analyze Multiple Projects
```bash
#!/bin/bash
# analyze_all.sh

projects=(
  "/path/to/project1"
  "/path/to/project2"
  "/path/to/project3"
)

for proj in "${projects[@]}"; do
  name=$(basename "$proj")
  echo "Analyzing $name..."
  cbig main -p "$proj" \
    --format json \
    -o "reports/${name}_analysis.json" \
    --cache-dir ".cache/${name}" \
    --quiet
done
```

### Progressive Analysis
```bash
# Quick overview first
cbig main -p . --format txt

# If interesting, get details
cbig main -p . --by-dir --output-dir detailed_analysis/

# If large, use cache
cbig main -p . --cache-dir .cbig_cache -j 8
```

### Incremental Updates
```bash
# Initial analysis
cbig main -p . --cache-dir .persistent_cache --by-dir

# Daily updates (uses cache)
cbig main -p . --cache-dir .persistent_cache --by-dir

# Weekly full refresh
cbig main -p . --cache-dir .persistent_cache --clear-cache --by-dir
```

## 🎨 OUTPUT CUSTOMIZATION EXAMPLES

### Custom Markdown Templates
```bash
# Timestamp in filename
cbig main -p . \
  --by-dir \
  --md-template "{{dir}}_{{suffix}}_$(date +%Y%m%d).md"

# Hierarchical naming
cbig main -p . \
  --by-dir \
  --md-template "analysis_{{dir|replace('/', '_')}}.md"
```

### Filtered Outputs
```bash
# Large functions only (for optimization)
cbig main -p . \
  --functions \
  --no-classes \
  --no-deps \
  --sort functions=size \
  --format md \
  -o large_functions.md

# Public API only
cbig main -p . \
  --include "**/public/*" \
  --include "**/api/*" \
  --functions \
  --classes
```

### Combined Analysis
```bash
# Structure + Metrics
cbig main -p . --format json -o structure.json --no-md
cbig main -p . --format yaml -o metrics.yaml --no-md
cbig main -p . --format md -o documentation.md

# Merge results in script
python merge_analysis.py structure.json metrics.yaml > full_report.json
```

## 🚀 PERFORMANCE OPTIMIZATION EXAMPLES

### Large Monorepo (>100k files)
```bash
# Step 1: Build cache gradually
cbig main -p src/ --cache-dir .cbig_cache -j 4
cbig main -p lib/ --cache-dir .cbig_cache -j 4
cbig main -p tests/ --cache-dir .cbig_cache -j 4

# Step 2: Full analysis with cache
cbig main -p . --cache-dir .cbig_cache -j 8 --by-dir
```

### Memory-Constrained System
```bash
# Sequential processing
cbig main -p . -j 1 --by-file

# Or process in chunks
find . -name "*.py" | head -100 | xargs cbig main -p
```

### Network Drive Analysis
```bash
# Copy locally first for speed
rsync -av remote:/project /tmp/local_copy/
cbig main -p /tmp/local_copy --cache-dir /tmp/cbig_cache
rm -rf /tmp/local_copy /tmp/cbig_cache
```

## 📝 SPECIAL SCENARIOS

### Analyzing Jupyter Notebooks
```bash
# Convert first if needed
jupyter nbconvert --to python *.ipynb
cbig main -p . -l python --include "*.py"
```

### Minified Code
```bash
# Skip minified files
cbig main -p . \
  --exclude "*.min.js" \
  --exclude "*.min.css" \
  --exclude "*-min.js"
```

### Archive Analysis
```bash
# Extract and analyze
unzip project.zip -d /tmp/project/
cbig main -p /tmp/project
rm -rf /tmp/project
```

### Git Repository Analysis
```bash
# Specific branch
git checkout feature-branch
cbig main -p . --cache-dir .cbig_cache

# Specific commit
git checkout abc123
cbig main -p . -o "analysis_abc123.md"
```

## 🎯 Quick One-Liners

```bash
# Count total functions
cbig main -p . --format json -o - | jq '.functions | length'

# List all Python files
cbig main -p . -l python --format json -o - | jq '.files[].path'

# Find largest file
cbig main -p . --format json -o - | jq '.files | max_by(.size)'

# Extract all TODOs (if comments enabled)
cbig main -p . --comments --format json -o - | grep -i "TODO"
```