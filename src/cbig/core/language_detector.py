"""Language detection for source files."""

import re
from pathlib import Path
from typing import Optional, List, Dict
import logging

from cbig.core.models import LANGUAGE_CONFIGS

logger = logging.getLogger(__name__)


class LanguageDetector:
    """Detects programming language of source files."""
    
    def __init__(self, enabled_languages: Optional[List[str]] = None):
        self.enabled_languages = set(enabled_languages) if enabled_languages else None
        
        # Build extension to language mapping
        self.extension_map = {}
        for lang_name, config in LANGUAGE_CONFIGS.items():
            if not config.enabled:
                continue
            if self.enabled_languages and lang_name not in self.enabled_languages:
                continue
            
            for ext in config.extensions:
                self.extension_map[ext.lower()] = lang_name
        
        # Content-based heuristics for ambiguous cases
        self.content_heuristics = {
            '.js': self._detect_js_variant,
            '.ts': self._detect_ts_variant,
            '.h': self._detect_c_variant,
        }
    
    def detect_language(self, file_path: Path) -> Optional[str]:
        """
        Detect the programming language of a file.
        
        Uses extension-based detection with content-based heuristics for ambiguous cases.
        """
        if not file_path.is_file():
            return None
        
        extension = file_path.suffix.lower()
        
        # Direct extension mapping
        if extension in self.extension_map:
            language = self.extension_map[extension]
            
            # Apply content heuristics if available
            if extension in self.content_heuristics:
                try:
                    refined_language = self.content_heuristics[extension](file_path)
                    if refined_language:
                        language = refined_language
                except Exception as e:
                    logger.debug(f"Heuristic failed for {file_path}: {e}")
            
            return language
        
        # Special cases for files without extensions
        if not extension:
            return self._detect_extensionless_file(file_path)
        
        return None
    
    def _detect_js_variant(self, file_path: Path) -> Optional[str]:
        """Detect JavaScript variants (.js could be Node, React, etc.)."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(2048)  # Read first 2KB
            
            # Look for React JSX patterns
            jsx_patterns = [
                r'import\s+React',
                r'from\s+["\']react["\']',
                r'<\w+.*?>.*?</\w+>',  # JSX tags
                r'className\s*=',
                r'jsx'
            ]
            
            if any(re.search(pattern, content, re.IGNORECASE) for pattern in jsx_patterns):
                return 'jsx'
            
            # Look for Node.js patterns
            node_patterns = [
                r'require\s*\(',
                r'module\.exports',
                r'process\.env',
                r'__dirname',
                r'__filename'
            ]
            
            if any(re.search(pattern, content) for pattern in node_patterns):
                return 'javascript'
            
            return 'javascript'
            
        except Exception:
            return 'javascript'
    
    def _detect_ts_variant(self, file_path: Path) -> Optional[str]:
        """Detect TypeScript variants (.ts vs .tsx)."""
        if file_path.suffix.lower() == '.tsx':
            return 'typescript'
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(2048)
            
            # Look for JSX in TypeScript
            jsx_patterns = [
                r'<\w+.*?>.*?</\w+>',
                r'jsx',
                r'React\.',
                r'import.*React'
            ]
            
            if any(re.search(pattern, content, re.IGNORECASE) for pattern in jsx_patterns):
                return 'typescript'  # Could be TSX but we'll treat as TypeScript
            
            return 'typescript'
            
        except Exception:
            return 'typescript'
    
    def _detect_c_variant(self, file_path: Path) -> Optional[str]:
        """Detect C vs C++ for .h files."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(2048)
            
            # Look for C++ specific patterns
            cpp_patterns = [
                r'#include\s+<iostream>',
                r'#include\s+<string>',
                r'#include\s+<vector>',
                r'std::',
                r'namespace\s+\w+',
                r'class\s+\w+',
                r'template\s*<',
                r'public\s*:',
                r'private\s*:',
                r'protected\s*:'
            ]
            
            if any(re.search(pattern, content) for pattern in cpp_patterns):
                return 'cpp'
            
            return 'c'
            
        except Exception:
            return 'c'
    
    def _detect_extensionless_file(self, file_path: Path) -> Optional[str]:
        """Detect language for files without extensions."""
        file_name = file_path.name.lower()
        
        # Common script names
        script_names = {
            'dockerfile': 'dockerfile',
            'makefile': 'makefile',
            'rakefile': 'ruby',
            'gemfile': 'ruby',
            'gruntfile': 'javascript',
            'gulpfile': 'javascript'
        }
        
        if file_name in script_names:
            return script_names[file_name]
        
        # Check shebang line
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                first_line = f.readline().strip()
            
            if first_line.startswith('#!'):
                shebang_map = {
                    'python': 'python',
                    'python3': 'python',
                    'node': 'javascript',
                    'bash': 'shell',
                    'sh': 'shell',
                    'ruby': 'ruby',
                    'perl': 'perl'
                }
                
                for interpreter, language in shebang_map.items():
                    if interpreter in first_line:
                        return language
        
        except Exception:
            pass
        
        return None
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages."""
        return list(self.extension_map.values())
    
    def get_extensions_for_language(self, language: str) -> List[str]:
        """Get file extensions for a given language."""
        config = LANGUAGE_CONFIGS.get(language)
        return config.extensions if config else []