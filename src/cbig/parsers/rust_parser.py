"""Rust language parser."""

import re
from typing import Dict, List, Any
from cbig.parsers.generic_parser import GenericParser


class RustParser(GenericParser):
    """Parser for Rust source code."""
    
    def __init__(self):
        super().__init__("rust")
    
    def extract_dependencies(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract Rust use statements and external crates."""
        dependencies = []
        
        patterns = [
            r'use\s+([a-zA-Z_][a-zA-Z0-9_:]*)',
            r'extern\s+crate\s+([a-zA-Z_][a-zA-Z0-9_]*)',
        ]
        
        for line in content.splitlines():
            line = line.strip()
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    dep_name = match.group(1)
                    # Extract root crate name
                    root_crate = dep_name.split('::')[0]
                    dependencies.append({
                        'language': 'rust',
                        'name': root_crate,
                        'version': None,
                        'source': 'cargo'
                    })
        
        return dependencies
    
    def extract_functions(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract Rust function definitions."""
        functions = []
        lines = content.splitlines()
        
        patterns = [
            r'^\s*(?:pub\s+)?(?:async\s+)?fn\s+(\w+)\s*\(',
            r'^\s*(?:pub\s+)?(?:unsafe\s+)?(?:extern\s+)?(?:async\s+)?fn\s+(\w+)\s*\(',
        ]
        
        for i, line in enumerate(lines):
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    func_name = match.group(1)
                    
                    signature = line.strip()
                    if len(signature) > 100:
                        signature = signature[:97] + "..."
                    
                    functions.append({
                        'language': 'rust',
                        'file': file_path,
                        'name': func_name,
                        'signature': signature,
                        'line_start': i + 1,
                        'line_end': i + 1,
                        'docstring': None,
                        'is_method': False,
                        'class_name': None
                    })
        
        return functions
    
    def extract_classes(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract Rust struct, enum, and trait definitions."""
        classes = []
        lines = content.splitlines()
        
        patterns = [
            (r'^\s*(?:pub\s+)?struct\s+(\w+)', 'struct'),
            (r'^\s*(?:pub\s+)?enum\s+(\w+)', 'enum'),
            (r'^\s*(?:pub\s+)?trait\s+(\w+)', 'trait'),
            (r'^\s*(?:pub\s+)?union\s+(\w+)', 'union'),
            (r'^\s*(?:pub\s+)?type\s+(\w+)', 'type')
        ]
        
        for i, line in enumerate(lines):
            for pattern, kind in patterns:
                match = re.search(pattern, line)
                if match:
                    item_name = match.group(1)
                    
                    # Extract trait bounds or inheritance-like info
                    inherits = None
                    implements = []
                    
                    if ':' in line and kind in ['struct', 'enum']:
                        # Look for trait implementations
                        colon_part = line.split(':', 1)[1].split('{')[0].strip()
                        if colon_part:
                            traits = [t.strip() for t in colon_part.split('+')]
                            implements = traits
                    
                    classes.append({
                        'language': 'rust',
                        'file': file_path,
                        'name': item_name,
                        'kind': kind,
                        'inherits': inherits,
                        'implements': implements,
                        'line_start': i + 1,
                        'line_end': i + 1,
                        'doc': None
                    })
        
        return classes