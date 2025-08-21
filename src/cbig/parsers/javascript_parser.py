"""JavaScript/TypeScript language parser."""

import re
from typing import Dict, List, Any
from cbig.parsers.generic_parser import GenericParser


class JavaScriptParser(GenericParser):
    """Parser for JavaScript and TypeScript source code."""
    
    def __init__(self):
        super().__init__("javascript")
    
    def extract_dependencies(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract JavaScript/TypeScript import statements."""
        dependencies = []
        
        patterns = [
            r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]',
            r'import\s+[\'"]([^\'"]+)[\'"]',
            r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)',
            r'import\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)'
        ]
        
        for line in content.splitlines():
            line = line.strip()
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    dep_name = match.group(1)
                    # Skip relative imports
                    if not dep_name.startswith('.'):
                        dependencies.append({
                            'language': 'javascript',
                            'name': dep_name,
                            'version': None,
                            'source': 'npm'
                        })
        
        return dependencies
    
    def extract_functions(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract JavaScript/TypeScript function definitions."""
        functions = []
        lines = content.splitlines()
        
        patterns = [
            r'^\s*function\s+(\w+)\s*\(',
            r'^\s*(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?function',
            r'^\s*(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(',
            r'^\s*(\w+)\s*:\s*(?:async\s+)?function',
            r'^\s*(?:async\s+)?(\w+)\s*\([^)]*\)\s*{',
            r'^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)',
        ]
        
        for i, line in enumerate(lines):
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    func_name = match.group(1)
                    
                    # Skip common keywords
                    if func_name in ['if', 'for', 'while', 'switch', 'try', 'catch', 'class']:
                        continue
                    
                    signature = line.strip()
                    if len(signature) > 100:
                        signature = signature[:97] + "..."
                    
                    functions.append({
                        'language': 'javascript',
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
        """Extract JavaScript/TypeScript class definitions."""
        classes = []
        lines = content.splitlines()
        
        patterns = [
            (r'^\s*(?:export\s+)?class\s+(\w+)', 'class'),
            (r'^\s*(?:export\s+)?interface\s+(\w+)', 'interface'),
            (r'^\s*(?:export\s+)?type\s+(\w+)', 'type'),
            (r'^\s*(?:export\s+)?enum\s+(\w+)', 'enum')
        ]
        
        for i, line in enumerate(lines):
            for pattern, kind in patterns:
                match = re.search(pattern, line)
                if match:
                    class_name = match.group(1)
                    
                    # Extract inheritance
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
                        'language': 'javascript',
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