"""Generic parser for languages without specific Tree-sitter support."""

import re
from typing import Dict, List, Any
import logging

from cbig.parsers.base import BaseParser

logger = logging.getLogger(__name__)


class GenericParser(BaseParser):
    """Generic parser that uses regex patterns for basic extraction."""
    
    def __init__(self, language: str = "generic"):
        self.language = language
        self.version = "1.0.0"
    
    def get_language(self) -> str:
        return self.language
    
    def get_version(self) -> str:
        return self.version
    
    def parse(self, content: str, file_path: str) -> Dict[str, Any]:
        """Parse source code using generic regex patterns."""
        return {
            'dependencies': self.extract_dependencies(content, file_path),
            'functions': self.extract_functions(content, file_path),
            'classes': self.extract_classes(content, file_path),
            'comments': self.extract_comments(content, file_path)
        }
    
    def extract_dependencies(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract import-like patterns."""
        dependencies = []
        
        # Common import patterns across languages
        patterns = [
            r'import\s+([a-zA-Z_][a-zA-Z0-9_./]*)',
            r'#include\s*[<"]([^>"]+)[>"]',
            r'require\s*\([\'"]([^\'"]+)[\'"]\)',
            r'from\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s+import',
            r'use\s+([a-zA-Z_][a-zA-Z0-9_:]*)',
        ]
        
        for line in content.splitlines():
            line = line.strip()
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    dep_name = match.group(1)
                    dependencies.append({
                        'language': self.language,
                        'name': dep_name,
                        'version': None,
                        'source': None
                    })
        
        return dependencies
    
    def extract_functions(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract function-like patterns."""
        functions = []
        lines = content.splitlines()
        
        # Common function patterns
        patterns = [
            r'^\s*(?:public|private|protected)?\s*(?:static)?\s*(?:async)?\s*function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
            r'^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
            r'^\s*(?:public|private|protected)?\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*{',
            r'^\s*fn\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
            r'^\s*func\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
        ]
        
        for i, line in enumerate(lines):
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    func_name = match.group(1)
                    
                    # Simple signature extraction
                    signature = line.strip()
                    if len(signature) > 100:
                        signature = signature[:97] + "..."
                    
                    functions.append({
                        'language': self.language,
                        'file': file_path,
                        'name': func_name,
                        'signature': signature,
                        'line_start': i + 1,
                        'line_end': i + 1,  # Simplified - just one line
                        'docstring': None,
                        'is_method': False,
                        'class_name': None
                    })
        
        return functions
    
    def extract_classes(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract class-like patterns."""
        classes = []
        lines = content.splitlines()
        
        # Common class patterns
        patterns = [
            r'^\s*class\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'^\s*struct\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'^\s*interface\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'^\s*enum\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'^\s*type\s+([a-zA-Z_][a-zA-Z0-9_]*)',
        ]
        
        for i, line in enumerate(lines):
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    class_name = match.group(1)
                    
                    # Determine kind from pattern
                    kind = "class"
                    if "struct" in line:
                        kind = "struct"
                    elif "interface" in line:
                        kind = "interface"
                    elif "enum" in line:
                        kind = "enum"
                    elif "type" in line:
                        kind = "type"
                    
                    classes.append({
                        'language': self.language,
                        'file': file_path,
                        'name': class_name,
                        'kind': kind,
                        'inherits': None,
                        'implements': [],
                        'line_start': i + 1,
                        'line_end': i + 1,  # Simplified
                        'doc': None
                    })
        
        return classes
    
    def extract_comments(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract comment blocks."""
        comments = []
        lines = content.splitlines()
        
        # Track comment blocks
        current_block = []
        current_start = None
        block_type = None
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Check for different comment styles
            is_comment = False
            comment_text = ""
            
            if stripped.startswith('//'):
                is_comment = True
                comment_text = stripped
                new_block_type = '//'
            elif stripped.startswith('#'):
                is_comment = True
                comment_text = stripped
                new_block_type = '#'
            elif stripped.startswith('/*') or (block_type == '/*' and not stripped.endswith('*/')):
                is_comment = True
                comment_text = stripped
                new_block_type = '/*'
            elif stripped.startswith('*') and block_type == '/*':
                is_comment = True
                comment_text = stripped
                new_block_type = '/*'
            
            if is_comment:
                if not current_block or block_type != new_block_type:
                    # Start new block
                    if current_block:
                        # Save previous block
                        self._save_comment_block(comments, current_block, current_start, i, file_path)
                    current_block = [comment_text]
                    current_start = i + 1
                    block_type = new_block_type
                else:
                    # Continue current block
                    current_block.append(comment_text)
            else:
                if current_block:
                    # End current block
                    self._save_comment_block(comments, current_block, current_start, i, file_path)
                    current_block = []
                    block_type = None
        
        # Handle trailing block
        if current_block:
            self._save_comment_block(comments, current_block, current_start, len(lines), file_path)
        
        return comments
    
    def _save_comment_block(self, comments: List, block: List[str], start: int, end: int, file_path: str):
        """Save a comment block to the results."""
        if len(block) >= 2:  # Only save multi-line comments
            comment_text = '\n'.join(block)
            comments.append({
                'language': self.language,
                'file': file_path,
                'line_start': start,
                'line_end': end,
                'text': comment_text
            })