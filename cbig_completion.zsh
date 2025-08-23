#compdef cbig

# CBIG ZSH Completion Script
# Provides intelligent autocomplete for cbig CLI

_cbig() {
    local -a options
    local -a formats
    local -a languages
    
    # Main command options
    options=(
        'main:Generate code insights'
        '--help:Show help message'
        '--install-completion:Install shell completion'
    )
    
    # Format options
    formats=(
        'json:Machine-readable JSON'
        'yaml:Human-readable YAML'
        'md:Markdown format'
        'txt:Plain text summary'
    )
    
    # Common language options
    languages=(
        'python:Python files'
        'javascript:JavaScript files'
        'typescript:TypeScript files'
        'java:Java files'
        'rust:Rust files'
        'html:HTML files'
    )
    
    # Main arguments
    _arguments \
        '(-p --path)'{-p,--path}'[Root path to analyze]:path:_files -/' \
        '(-l --language)'{-l,--language}'[Languages to include (comma-separated)]:languages:' \
        '(-f --format)'{-f,--format}'[Output format]:format:(json yaml md txt)' \
        '(-o --out)'{-o,--out}'[Output file]:file:_files' \
        '(-j --max-workers)'{-j,--max-workers}'[Number of parallel workers]:workers:' \
        '--by-dir[Generate one markdown per directory]' \
        '--by-file[Generate one markdown per file]' \
        '--output-dir[Output directory for markdown files]:dir:_files -/' \
        '--cache-dir[Cache directory for AST]:dir:_files -/' \
        '--exclude[Patterns to exclude]:pattern:' \
        '--include[Patterns to include]:pattern:' \
        '--no-md[Skip markdown generation]' \
        '--no-functions[Exclude functions from output]' \
        '--no-classes[Exclude classes from output]' \
        '--no-deps[Exclude dependencies from output]' \
        '--comments[Include comments in output]' \
        '--clear-cache[Clear cache before processing]' \
        '(-v --verbose)'{-v,--verbose}'[Verbose output]' \
        '(-q --quiet)'{-q,--quiet}'[Quiet mode]' \
        '--help[Show help message]' \
        '*:path:_files -/'
}

compdef _cbig cbig