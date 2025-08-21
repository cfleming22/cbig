"""Python language parser using Tree-sitter."""

import re
from typing import Dict, List, Any
import logging

try:
    import tree_sitter
    import tree_sitter_python as tspython
    TREE_SITTER_AVAILABLE = True
except ImportError:
    TREE_SITTER_AVAILABLE = False

from cbig.parsers.base import BaseParser

logger = logging.getLogger(__name__)


class PythonParser(BaseParser):
    """Parser for Python source code."""
    
    def __init__(self):
        self.language = "python"
        self.version = "1.0.0"
        
        if TREE_SITTER_AVAILABLE:
            try:
                self.ts_language = tree_sitter.Language(tspython.language())
                self.parser = tree_sitter.Parser(self.ts_language)
                self.tree_sitter_enabled = True
                logger.debug("Tree-sitter Python parser initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Tree-sitter Python parser: {e}")
                self.tree_sitter_enabled = False
        else:
            self.tree_sitter_enabled = False
            logger.warning("Tree-sitter not available, falling back to regex parsing")
    
    def get_language(self) -> str:
        return self.language
    
    def get_version(self) -> str:
        return self.version
    
    def parse(self, content: str, file_path: str) -> Dict[str, Any]:
        """Parse Python source code."""
        if self.tree_sitter_enabled:
            return self._parse_with_tree_sitter(content, file_path)
        else:
            return self._parse_with_regex(content, file_path)
    
    def _parse_with_tree_sitter(self, content: str, file_path: str) -> Dict[str, Any]:
        """Parse using Tree-sitter for accurate AST parsing."""
        try:
            tree = self.parser.parse(content.encode('utf-8'))
            root = tree.root_node
            
            return {
                'dependencies': self._extract_imports_ts(root, content),
                'functions': self._extract_functions_ts(root, content, file_path),
                'classes': self._extract_classes_ts(root, content, file_path),
                'comments': self._extract_comments_ts(root, content, file_path)
            }
        except Exception as e:
            logger.error(f"Tree-sitter parsing failed for {file_path}: {e}")
            return self._parse_with_regex(content, file_path)
    
    def _extract_imports_ts(self, root, content: str) -> List[Dict[str, Any]]:
        """Extract import statements using Tree-sitter."""
        imports = []
        lines = content.splitlines()
        
        def walk_tree(node):
            if node.type == 'import_statement':
                # import module
                for child in node.children:
                    if child.type == 'dotted_name' or child.type == 'identifier':
                        module_name = content[child.start_byte:child.end_byte]
                        imports.append({
                            'language': 'python',
                            'name': module_name,
                            'version': None,
                            'source': 'pip'
                        })
            elif node.type == 'import_from_statement':
                # from module import ...
                module_node = None
                for child in node.children:
                    if child.type == 'dotted_name' or child.type == 'identifier':
                        if content[child.start_byte:child.end_byte] != 'import':
                            module_node = child
                            break
                
                if module_node:
                    module_name = content[module_node.start_byte:module_node.end_byte]
                    imports.append({
                        'language': 'python',
                        'name': module_name,
                        'version': None,
                        'source': 'pip'
                    })
            
            for child in node.children:
                walk_tree(child)
        
        walk_tree(root)
        return imports
    
    def _extract_functions_ts(self, root, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract function definitions using Tree-sitter."""
        functions = []
        lines = content.splitlines()
        
        def walk_tree(node, class_name=None):
            if node.type == 'function_definition':
                name_node = None
                params_node = None
                
                for child in node.children:
                    if child.type == 'identifier':
                        name_node = child
                    elif child.type == 'parameters':
                        params_node = child
                
                if name_node:
                    func_name = content[name_node.start_byte:name_node.end_byte]
                    
                    # Build signature
                    if params_node:
                        params = content[params_node.start_byte:params_node.end_byte]
                    else:
                        params = "()"
                    
                    signature = f"def {func_name}{params}"
                    
                    # Extract docstring
                    docstring = self._extract_docstring_ts(node, content)
                    
                    functions.append({
                        'language': 'python',
                        'file': file_path,
                        'name': func_name,
                        'signature': signature,
                        'line_start': node.start_point[0] + 1,
                        'line_end': node.end_point[0] + 1,
                        'docstring': docstring,
                        'is_method': class_name is not None,
                        'class_name': class_name
                    })
            elif node.type == 'class_definition':
                # Find class name
                class_name_node = None
                for child in node.children:
                    if child.type == 'identifier':
                        class_name_node = child
                        break
                
                current_class = None
                if class_name_node:
                    current_class = content[class_name_node.start_byte:class_name_node.end_byte]
                
                # Continue walking to find methods
                for child in node.children:
                    walk_tree(child, current_class)
            else:
                for child in node.children:
                    walk_tree(child, class_name)
        
        walk_tree(root)
        return functions
    
    def _extract_classes_ts(self, root, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract class definitions using Tree-sitter."""
        classes = []
        
        def walk_tree(node):
            if node.type == 'class_definition':
                name_node = None
                bases_node = None
                
                for child in node.children:
                    if child.type == 'identifier':
                        name_node = child
                    elif child.type == 'argument_list':
                        bases_node = child
                
                if name_node:
                    class_name = content[name_node.start_byte:name_node.end_byte]
                    
                    # Extract inheritance
                    inherits = None
                    if bases_node:
                        bases_text = content[bases_node.start_byte:bases_node.end_byte]
                        bases_text = bases_text.strip('()')
                        if bases_text:
                            inherits = bases_text.split(',')[0].strip()
                    
                    # Extract docstring
                    docstring = self._extract_docstring_ts(node, content)
                    
                    classes.append({
                        'language': 'python',
                        'file': file_path,
                        'name': class_name,
                        'kind': 'class',
                        'inherits': inherits,
                        'implements': [],
                        'line_start': node.start_point[0] + 1,
                        'line_end': node.end_point[0] + 1,
                        'doc': docstring
                    })
            
            for child in node.children:
                walk_tree(child)
        
        walk_tree(root)
        return classes
    
    def _extract_comments_ts(self, root, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract top-level comments using Tree-sitter."""
        comments = []
        lines = content.splitlines()
        
        def walk_tree(node):
            if node.type == 'comment':
                line_start = node.start_point[0] + 1
                line_end = node.end_point[0] + 1
                text = content[node.start_byte:node.end_byte]
                
                comments.append({
                    'language': 'python',
                    'file': file_path,
                    'line_start': line_start,
                    'line_end': line_end,
                    'text': text
                })
            
            for child in node.children:
                walk_tree(child)
        
        walk_tree(root)
        return comments
    
    def _extract_docstring_ts(self, node, content: str) -> str:
        """Extract docstring from a function or class node."""
        # Look for string literal as first statement in body
        for child in node.children:
            if child.type == 'block':
                for stmt in child.children:
                    if stmt.type == 'expression_statement':
                        for expr_child in stmt.children:
                            if expr_child.type == 'string':
                                docstring = content[expr_child.start_byte:expr_child.end_byte]
                                # Clean up quotes and format
                                docstring = docstring.strip('\'"')
                                return docstring
                break
        return None
    
    def _parse_with_regex(self, content: str, file_path: str) -> Dict[str, Any]:
        """Fallback regex-based parsing when Tree-sitter is not available."""
        return {
            'dependencies': self._extract_imports_regex(content),
            'functions': self._extract_functions_regex(content, file_path),
            'classes': self._extract_classes_regex(content, file_path),
            'comments': self._extract_comments_regex(content, file_path)
        }
    
    def _extract_imports_regex(self, content: str) -> List[Dict[str, Any]]:
        """Extract imports using regex patterns."""
        imports = []
        
        # Match import statements
        import_patterns = [
            r'^import\s+([a-zA-Z_][a-zA-Z0-9_.]*)',
            r'^from\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s+import'
        ]
        
        for line in content.splitlines():
            line = line.strip()
            for pattern in import_patterns:
                match = re.match(pattern, line)
                if match:
                    module_name = match.group(1)
                    imports.append({
                        'language': 'python',
                        'name': module_name,
                        'version': None,
                        'source': 'pip'
                    })
        
        return imports
    
    def _extract_functions_regex(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract functions using regex patterns."""
        functions = []
        lines = content.splitlines()
        
        func_pattern = r'^(\s*)def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\):'
        
        for i, line in enumerate(lines):
            match = re.match(func_pattern, line)
            if match:
                indent, func_name, params = match.groups()
                signature = f"def {func_name}({params})"
                
                # Find end of function (simplified)
                end_line = i + 1
                base_indent = len(indent)
                for j in range(i + 1, len(lines)):
                    if lines[j].strip() and not lines[j].startswith(' ' * (base_indent + 1)):
                        end_line = j
                        break
                
                functions.append({
                    'language': 'python',
                    'file': file_path,
                    'name': func_name,
                    'signature': signature,
                    'line_start': i + 1,
                    'line_end': end_line,
                    'docstring': None,
                    'is_method': False,
                    'class_name': None
                })
        
        return functions
    
    def _extract_classes_regex(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract classes using regex patterns."""
        classes = []
        lines = content.splitlines()
        
        class_pattern = r'^(\s*)class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:\((.*?)\))?:'
        
        for i, line in enumerate(lines):
            match = re.match(class_pattern, line)
            if match:
                indent, class_name, bases = match.groups()
                
                # Find end of class (simplified)
                end_line = i + 1
                base_indent = len(indent)
                for j in range(i + 1, len(lines)):
                    if lines[j].strip() and not lines[j].startswith(' ' * (base_indent + 1)):
                        end_line = j
                        break
                
                inherits = None
                if bases and bases.strip():
                    inherits = bases.split(',')[0].strip()
                
                classes.append({
                    'language': 'python',
                    'file': file_path,
                    'name': class_name,
                    'kind': 'class',
                    'inherits': inherits,
                    'implements': [],
                    'line_start': i + 1,
                    'line_end': end_line,
                    'doc': None
                })
        
        return classes
    
    def _extract_comments_regex(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract comments using regex patterns."""
        comments = []
        lines = content.splitlines()
        
        comment_blocks = []
        current_block = []
        current_start = None
        
        for i, line in enumerate(lines):
            if line.strip().startswith('#'):
                if not current_block:
                    current_start = i + 1
                current_block.append(line)
            else:
                if current_block:
                    comment_text = '\n'.join(current_block)
                    comments.append({
                        'language': 'python',
                        'file': file_path,
                        'line_start': current_start,
                        'line_end': i,
                        'text': comment_text
                    })
                    current_block = []
        
        # Handle trailing comment block
        if current_block:
            comment_text = '\n'.join(current_block)
            comments.append({
                'language': 'python',
                'file': file_path,
                'line_start': current_start,
                'line_end': len(lines),
                'text': comment_text
            })
        
        return comments