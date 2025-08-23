#!/bin/bash
# CBIG Convenient Aliases and Functions
# Add this to your ~/.zshrc or ~/.bashrc

# Basic CBIG commands
alias cbig-here='cbig main -p .'
alias cbig-docs='cbig main -p . --by-dir --output-dir docs/'
alias cbig-fast='cbig main -p . --cache-dir .cbig_cache -j 8'
alias cbig-json='cbig main -p . --format json -o analysis.json --no-md'
alias cbig-yaml='cbig main -p . --format yaml -o analysis.yaml --no-md'

# Language-specific shortcuts
alias cbig-py='cbig main -p . -l python'
alias cbig-js='cbig main -p . -l javascript,typescript'
alias cbig-web='cbig main -p . -l javascript,typescript,html,css'
alias cbig-java='cbig main -p . -l java'
alias cbig-rust='cbig main -p . -l rust'

# Advanced CBIG function for easy path analysis
cbig-analyze() {
    local path="${1:-.}"
    local output_dir="${2:-${path}/cbig_docs}"
    
    echo "🔍 Analyzing: $path"
    echo "📁 Output to: $output_dir"
    
    cbig main -p "$path" \
        --by-dir \
        --output-dir "$output_dir" \
        --cache-dir "${path}/.cbig_cache" \
        -j 8 \
        --exclude "node_modules/*" \
        --exclude "build/*" \
        --exclude "dist/*" \
        --exclude ".git/*"
    
    echo "✅ Analysis complete! Check $output_dir"
}

# Quick single file analysis
cbig-file() {
    if [ -z "$1" ]; then
        echo "Usage: cbig-file <filename>"
        return 1
    fi
    cbig main -p "$1" --by-file
}

# Generate AI-ready context file
cbig-ai() {
    local path="${1:-.}"
    local output="${2:-ai_context.md}"
    
    echo "🤖 Generating AI context for: $path"
    cbig main -p "$path" \
        --format md \
        -o "$output" \
        --comments \
        --cache-dir .cbig_cache
    
    echo "✅ AI context saved to: $output"
}

# Quick summary to terminal
cbig-summary() {
    cbig main -p "${1:-.}" --format txt
}

# List all functions for reference
cbig-help() {
    echo "CBIG Quick Commands:"
    echo "  cbig <path>           - Analyze any directory"
    echo "  cbig-here            - Analyze current directory"
    echo "  cbig-docs            - Generate documentation in docs/"
    echo "  cbig-fast            - Fast cached analysis with 8 workers"
    echo "  cbig-json            - Export to JSON"
    echo "  cbig-yaml            - Export to YAML"
    echo ""
    echo "Language-specific:"
    echo "  cbig-py              - Python only"
    echo "  cbig-js              - JavaScript/TypeScript only"
    echo "  cbig-web             - Web files (JS/TS/HTML/CSS)"
    echo "  cbig-java            - Java only"
    echo "  cbig-rust            - Rust only"
    echo ""
    echo "Functions:"
    echo "  cbig-analyze <path> [output_dir] - Full analysis with caching"
    echo "  cbig-file <file>                 - Analyze single file"
    echo "  cbig-ai <path> [output]          - Generate AI context file"
    echo "  cbig-summary <path>              - Quick text summary"
    echo ""
    echo "Examples:"
    echo "  cbig ~/my-project                - Basic analysis"
    echo "  cbig-analyze ~/my-project         - Full cached analysis"
    echo "  cbig-ai . context.md              - Create AI context file"
}