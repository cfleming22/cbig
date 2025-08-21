"""File walker that discovers source files while respecting gitignore and patterns."""

import os
from pathlib import Path
from typing import List, Iterator, Set
import pathspec
import logging

logger = logging.getLogger(__name__)


class FileWalker:
    """Walks directory trees to discover source files with pattern filtering."""
    
    def __init__(self, include_patterns: List[str] = None, exclude_patterns: List[str] = None):
        self.include_patterns = include_patterns or []
        self.exclude_patterns = exclude_patterns or []
        
        # Default exclusions for common non-source directories
        self.default_excludes = [
            ".git/**",
            ".svn/**",
            ".hg/**",
            "node_modules/**",
            "__pycache__/**",
            "*.pyc",
            ".pytest_cache/**",
            "venv/**",
            ".venv/**",
            "env/**",
            ".env/**",
            "target/**",  # Rust
            "build/**",
            "dist/**",
            "*.egg-info/**",
            ".tox/**",
            "coverage/**",
            ".coverage/**",
            ".nyc_output/**",
            "logs/**",
            "*.log",
            "*.tmp",
            "*.temp",
            ".DS_Store",
            "Thumbs.db",
            ".idea/**",
            ".vscode/**",
            "*.min.js",
            "*.min.css"
        ]
        
        # Compile pathspecs
        self._setup_pathspecs()
    
    def _setup_pathspecs(self):
        """Setup pathspec matchers for include/exclude patterns."""
        # Combine default excludes with user excludes
        all_excludes = self.default_excludes + self.exclude_patterns
        
        self.exclude_spec = pathspec.PathSpec.from_lines('gitwildmatch', all_excludes)
        
        if self.include_patterns:
            self.include_spec = pathspec.PathSpec.from_lines('gitwildmatch', self.include_patterns)
        else:
            self.include_spec = None
    
    def walk(self, root_path: Path) -> Iterator[Path]:
        """
        Walk the directory tree starting from root_path.
        
        Yields file paths that match the filtering criteria.
        """
        if not root_path.exists():
            logger.error(f"Path does not exist: {root_path}")
            return
        
        if root_path.is_file():
            # Single file
            if self._should_include_file(root_path, root_path.parent):
                yield root_path
            return
        
        # Load gitignore if present
        gitignore_spec = self._load_gitignore(root_path)
        
        # Walk directory tree
        for dir_path, dir_names, file_names in os.walk(root_path):
            current_dir = Path(dir_path)
            relative_dir = current_dir.relative_to(root_path)
            
            # Check if directory should be excluded
            if self._should_exclude_directory(relative_dir):
                dir_names.clear()  # Don't recurse into excluded directories
                continue
            
            # Process files in current directory
            for file_name in file_names:
                file_path = current_dir / file_name
                relative_file = file_path.relative_to(root_path)
                
                # Apply all filters
                if (self._should_include_file(file_path, root_path) and
                    not self._is_gitignored(relative_file, gitignore_spec)):
                    yield file_path
    
    def _should_include_file(self, file_path: Path, root_path: Path) -> bool:
        """Check if a file should be included based on patterns."""
        try:
            relative_path = file_path.relative_to(root_path)
        except ValueError:
            # File is not under root_path
            relative_path = file_path
        
        relative_str = str(relative_path)
        
        # Check exclude patterns
        if self.exclude_spec.match_file(relative_str):
            return False
        
        # Check include patterns (if specified)
        if self.include_spec:
            return self.include_spec.match_file(relative_str)
        
        # Default: include files that look like source code
        return self._is_source_file(file_path)
    
    def _should_exclude_directory(self, dir_path: Path) -> bool:
        """Check if a directory should be excluded."""
        dir_str = str(dir_path)
        if dir_str == ".":
            return False
        
        return self.exclude_spec.match_file(dir_str + "/")
    
    def _is_source_file(self, file_path: Path) -> bool:
        """Check if a file appears to be source code based on extension."""
        source_extensions = {
            '.py', '.pyi',           # Python
            '.java',                 # Java
            '.js', '.jsx', '.mjs', '.cjs',  # JavaScript
            '.ts', '.tsx',           # TypeScript
            '.html', '.htm',         # HTML
            '.rs',                   # Rust
            '.swift',                # Swift
            '.c', '.h',              # C
            '.cpp', '.cc', '.cxx', '.hpp',  # C++
            '.go',                   # Go
            '.rb',                   # Ruby
            '.php',                  # PHP
            '.cs',                   # C#
            '.kt',                   # Kotlin
            '.scala',                # Scala
            '.sh', '.bash',          # Shell
            '.sql',                  # SQL
            '.xml',                  # XML
            '.json',                 # JSON
            '.yaml', '.yml',         # YAML
            '.toml',                 # TOML
            '.md', '.markdown',      # Markdown
            '.txt',                  # Text
            '.cfg', '.conf', '.ini', # Config files
            '.dockerfile', '.Dockerfile'  # Docker
        }
        
        return file_path.suffix.lower() in source_extensions
    
    def _load_gitignore(self, root_path: Path) -> pathspec.PathSpec:
        """Load .gitignore patterns if available."""
        gitignore_path = root_path / '.gitignore'
        
        if not gitignore_path.exists():
            return pathspec.PathSpec([])
        
        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                patterns = f.read().splitlines()
            
            # Filter out comments and empty lines
            patterns = [
                line.strip() for line in patterns
                if line.strip() and not line.strip().startswith('#')
            ]
            
            return pathspec.PathSpec.from_lines('gitwildmatch', patterns)
        
        except Exception as e:
            logger.warning(f"Failed to read .gitignore: {e}")
            return pathspec.PathSpec([])
    
    def _is_gitignored(self, relative_path: Path, gitignore_spec: pathspec.PathSpec) -> bool:
        """Check if a file is ignored by gitignore patterns."""
        if not gitignore_spec:
            return False
        
        # Check file path
        if gitignore_spec.match_file(str(relative_path)):
            return True
        
        # Check if any parent directory is ignored
        for parent in relative_path.parents:
            if parent == Path('.'):
                break
            if gitignore_spec.match_file(str(parent) + '/'):
                return True
        
        return False