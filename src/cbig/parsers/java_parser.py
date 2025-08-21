"""Java language parser."""

import re
from typing import Dict, List, Any
from cbig.parsers.generic_parser import GenericParser


class JavaParser(GenericParser):
    """Parser for Java source code."""
    
    def __init__(self):
        super().__init__("java")
    
    def extract_dependencies(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract Java import statements."""
        dependencies = []
        
        patterns = [
            r'import\s+(?:static\s+)?([a-zA-Z_][a-zA-Z0-9_.]*)',
            r'package\s+([a-zA-Z_][a-zA-Z0-9_.]*)'
        ]
        
        for line in content.splitlines():
            line = line.strip()
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    dep_name = match.group(1)
                    dependencies.append({
                        'language': 'java',
                        'name': dep_name,
                        'version': None,
                        'source': 'maven'
                    })
        
        return dependencies
    
    def extract_functions(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract Java method definitions."""
        functions = []
        lines = content.splitlines()
        
        # Java method pattern
        method_pattern = r'^\s*(?:public|private|protected)?\s*(?:static)?\s*(?:final)?\s*(?:\w+\s+)?(\w+)\s*\([^)]*\)\s*(?:throws\s+\w+)?\s*{'
        
        for i, line in enumerate(lines):
            match = re.search(method_pattern, line)
            if match:
                method_name = match.group(1)
                
                # Skip constructors and common non-method patterns
                if method_name in ['if', 'for', 'while', 'switch', 'try', 'catch']:
                    continue
                
                signature = line.strip()
                if len(signature) > 100:
                    signature = signature[:97] + "..."
                
                functions.append({
                    'language': 'java',
                    'file': file_path,
                    'name': method_name,
                    'signature': signature,
                    'line_start': i + 1,
                    'line_end': i + 1,
                    'docstring': None,
                    'is_method': True,
                    'class_name': None
                })
        
        return functions
    
    def extract_classes(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract Java class definitions."""
        classes = []
        lines = content.splitlines()
        
        # Java class patterns
        patterns = [
            (r'^\s*(?:public|private|protected)?\s*(?:static)?\s*(?:final)?\s*class\s+(\w+)', 'class'),
            (r'^\s*(?:public|private|protected)?\s*(?:static)?\s*interface\s+(\w+)', 'interface'),
            (r'^\s*(?:public|private|protected)?\s*(?:static)?\s*enum\s+(\w+)', 'enum'),
            (r'^\s*(?:public|private|protected)?\s*(?:static)?\s*@interface\s+(\w+)', 'annotation')
        ]
        
        for i, line in enumerate(lines):
            for pattern, kind in patterns:
                match = re.search(pattern, line)
                if match:
                    class_name = match.group(1)
                    
                    # Extract inheritance/implementation
                    inherits = None
                    implements = []
                    
                    if 'extends' in line:
                        extends_match = re.search(r'extends\s+(\w+)', line)
                        if extends_match:
                            inherits = extends_match.group(1)
                    
                    if 'implements' in line:
                        implements_match = re.search(r'implements\s+([^{]+)', line)
                        if implements_match:
                            impl_text = implements_match.group(1).strip()
                            implements = [iface.strip() for iface in impl_text.split(',')]
                    
                    classes.append({
                        'language': 'java',
                        'file': file_path,
                        'name': class_name,
                        'kind': kind,
                        'inherits': inherits,
                        'implements': implements,
                        'line_start': i + 1,
                        'line_end': i + 1,
                        'doc': None
                    })
        
        return classes