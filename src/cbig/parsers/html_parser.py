"""HTML language parser."""

import re
from typing import Dict, List, Any
from cbig.parsers.generic_parser import GenericParser


class HTMLParser(GenericParser):
    """Parser for HTML source code."""
    
    def __init__(self):
        super().__init__("html")
    
    def extract_dependencies(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract HTML dependencies (scripts, stylesheets, etc.)."""
        dependencies = []
        
        patterns = [
            r'<script[^>]*src=[\'"]([^\'"]+)[\'"]',
            r'<link[^>]*href=[\'"]([^\'"]+\.css)[\'"]',
            r'<link[^>]*href=[\'"]([^\'"]+)[\'"][^>]*rel=[\'"]stylesheet[\'"]',
            r'@import\s+[\'"]([^\'"]+)[\'"]',
        ]
        
        for line in content.splitlines():
            for pattern in patterns:
                matches = re.findall(pattern, line, re.IGNORECASE)
                for match in matches:
                    # Skip data URLs and inline scripts
                    if not match.startswith(('data:', 'javascript:', '#')):
                        dependencies.append({
                            'language': 'html',
                            'name': match,
                            'version': None,
                            'source': 'web'
                        })
        
        return dependencies
    
    def extract_functions(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract JavaScript functions embedded in HTML."""
        functions = []
        lines = content.splitlines()
        
        in_script = False
        script_content = []
        script_start = 0
        
        for i, line in enumerate(lines):
            if '<script' in line.lower():
                in_script = True
                script_start = i + 1
                script_content = []
            elif '</script>' in line.lower():
                in_script = False
                if script_content:
                    # Parse JavaScript in script content
                    js_content = '\n'.join(script_content)
                    js_functions = self._extract_js_functions_from_content(js_content, file_path, script_start)
                    functions.extend(js_functions)
            elif in_script:
                script_content.append(line)
        
        return functions
    
    def _extract_js_functions_from_content(self, content: str, file_path: str, start_line: int) -> List[Dict[str, Any]]:
        """Extract JavaScript functions from script content."""
        functions = []
        lines = content.splitlines()
        
        patterns = [
            r'function\s+(\w+)\s*\(',
            r'(?:const|let|var)\s+(\w+)\s*=\s*function',
            r'(\w+)\s*:\s*function'
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
                        'language': 'html',
                        'file': file_path,
                        'name': func_name,
                        'signature': signature,
                        'line_start': start_line + i,
                        'line_end': start_line + i,
                        'docstring': None,
                        'is_method': False,
                        'class_name': None
                    })
        
        return functions
    
    def extract_classes(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract HTML elements as 'classes' (custom elements, components)."""
        classes = []
        lines = content.splitlines()
        
        # Look for custom elements and web components
        custom_element_pattern = r'<([a-z]+-[a-z-]+)'
        
        found_elements = set()
        for i, line in enumerate(lines):
            matches = re.findall(custom_element_pattern, line, re.IGNORECASE)
            for match in matches:
                if match not in found_elements:
                    found_elements.add(match)
                    classes.append({
                        'language': 'html',
                        'file': file_path,
                        'name': match,
                        'kind': 'custom-element',
                        'inherits': None,
                        'implements': [],
                        'line_start': i + 1,
                        'line_end': i + 1,
                        'doc': None
                    })
        
        return classes