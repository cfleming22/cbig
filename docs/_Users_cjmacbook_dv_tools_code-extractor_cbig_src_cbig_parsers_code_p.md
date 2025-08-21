# /Users/cjmacbook/dv/tools/code-extractor/cbig/src/cbig/parsers – python Overview

---

## 📦 Libraries / Imports

| Library / Package | Version | Source | Language |
|-------------------|---------|--------|-----------|
| abc | – | pip | python |
| cbig.parsers.base | – | pip | python |
| cbig.parsers.base | – | pip | python |
| cbig.parsers.base | – | pip | python |
| cbig.parsers.generic_parser | – | pip | python |
| cbig.parsers.generic_parser | – | pip | python |
| cbig.parsers.generic_parser | – | pip | python |
| cbig.parsers.generic_parser | – | pip | python |
| cbig.parsers.generic_parser | – | pip | python |
| cbig.parsers.html_parser | – | pip | python |
| cbig.parsers.java_parser | – | pip | python |
| cbig.parsers.javascript_parser | – | pip | python |
| cbig.parsers.python_parser | – | pip | python |
| cbig.parsers.rust_parser | – | pip | python |
| logging | – | pip | python |
| logging | – | pip | python |
| logging | – | pip | python |
| logging | – | pip | python |
| re | – | pip | python |
| re | – | pip | python |
| re | – | pip | python |
| re | – | pip | python |
| re | – | pip | python |
| re | – | pip | python |
| tree_sitter | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |

---

## 🔧 Functions / Methods

| Name | Signature | Lines | File | Docstring |
|------|-----------|-------|------|-----------|
| __init__ | `def __init__(self)` | 11–12 | rust_parser.py | – |
| __init__ | `def __init__(self)` | 11–12 | html_parser.py | – |
| __init__ | `def __init__(self)` | 11–12 | java_parser.py | – |
| __init__ | `def __init__(self)` | 11–12 | javascript_parser.py | – |
| __init__ | `def __init__(self)` | 20–22 | registry.py | – |
| __init__ | `def __init__(self, language: str = "generic")` | 15–17 | generic_parser.py | – |
| __init__ | `def __init__(self)` | 22–37 | python_parser.py | – |
| _empty_result | `def _empty_result(self)` | 88–95 | base.py | Return empty parsing result. |
| _extract_classes_regex | `def _extract_classes_regex(self, content: str, file_path: str)` | 329–365 | python_parser.py | Extract classes using regex patterns. |
| _extract_classes_ts | `def _extract_classes_ts(self, root, content: str, file_path: str)` | 172–217 | python_parser.py | Extract class definitions using Tree-sitter. |
| _extract_comments_regex | `def _extract_comments_regex(self, content: str, file_path: str)` | 367–404 | python_parser.py | Extract comments using regex patterns. |
| _extract_comments_ts | `def _extract_comments_ts(self, root, content: str, file_path: str)` | 219–242 | python_parser.py | Extract top-level comments using Tree-sitter. |
| _extract_docstring_ts | `def _extract_docstring_ts(self, node, content: str)` | 244–258 | python_parser.py | Extract docstring from a function or class node. |
| _extract_functions_regex | `def _extract_functions_regex(self, content: str, file_path: str)` | 294–327 | python_parser.py | Extract functions using regex patterns. |
| _extract_functions_ts | `def _extract_functions_ts(self, root, content: str, file_path: str)` | 109–170 | python_parser.py | Extract function definitions using Tree-sitter. |
| _extract_imports_regex | `def _extract_imports_regex(self, content: str)` | 269–292 | python_parser.py | Extract imports using regex patterns. |
| _extract_imports_ts | `def _extract_imports_ts(self, root, content: str)` | 68–107 | python_parser.py | Extract import statements using Tree-sitter. |
| _extract_js_functions_from_content | `def _extract_js_functions_from_content(self, content: str, file_path: str, st...` | 66–99 | html_parser.py | Extract JavaScript functions from script content. |
| _initialize_parsers | `def _initialize_parsers(self)` | 24–44 | registry.py | Initialize all available parsers. |
| _parse_with_regex | `def _parse_with_regex(self, content: str, file_path: str)` | 260–267 | python_parser.py | Fallback regex-based parsing when Tree-sitter i... |
| _parse_with_tree_sitter | `def _parse_with_tree_sitter(self, content: str, file_path: str)` | 52–66 | python_parser.py | Parse using Tree-sitter for accurate AST parsing. |
| _safe_parse | `def _safe_parse(self, content: str, file_path: str)` | 66–86 | base.py | 
        Safely parse content with error handli... |
| _save_comment_block | `def _save_comment_block(self, comments: List, block: List[str], start: int, e...` | 205–215 | generic_parser.py | Save a comment block to the results. |
| extract_classes | `def extract_classes(self, content: str, file_path: str)` | 74–116 | rust_parser.py | Extract Rust struct, enum, and trait definitions. |
| extract_classes | `def extract_classes(self, content: str, file_path: str)` | 101–127 | html_parser.py | Extract HTML elements as 'classes' (custom elem... |
| extract_classes | `def extract_classes(self, content: str, file_path: str)` | 58–60 | base.py | Extract class/type definitions. |
| extract_classes | `def extract_classes(self, content: str, file_path: str)` | 73–119 | java_parser.py | Extract Java class definitions. |
| extract_classes | `def extract_classes(self, content: str, file_path: str)` | 84–129 | javascript_parser.py | Extract JavaScript/TypeScript class definitions. |
| extract_classes | `def extract_classes(self, content: str, file_path: str)` | 101–144 | generic_parser.py | Extract class-like patterns. |
| extract_comments | `def extract_comments(self, content: str, file_path: str)` | 62–64 | base.py | Extract top-level comments. |
| extract_comments | `def extract_comments(self, content: str, file_path: str)` | 146–203 | generic_parser.py | Extract comment blocks. |
| extract_dependencies | `def extract_dependencies(self, content: str, file_path: str)` | 14–38 | rust_parser.py | Extract Rust use statements and external crates. |
| extract_dependencies | `def extract_dependencies(self, content: str, file_path: str)` | 14–38 | html_parser.py | Extract HTML dependencies (scripts, stylesheets... |
| extract_dependencies | `def extract_dependencies(self, content: str, file_path: str)` | 50–52 | base.py | Extract import/dependency information. |
| extract_dependencies | `def extract_dependencies(self, content: str, file_path: str)` | 14–36 | java_parser.py | Extract Java import statements. |
| extract_dependencies | `def extract_dependencies(self, content: str, file_path: str)` | 14–40 | javascript_parser.py | Extract JavaScript/TypeScript import statements. |
| extract_dependencies | `def extract_dependencies(self, content: str, file_path: str)` | 34–60 | generic_parser.py | Extract import-like patterns. |
| extract_functions | `def extract_functions(self, content: str, file_path: str)` | 40–72 | rust_parser.py | Extract Rust function definitions. |
| extract_functions | `def extract_functions(self, content: str, file_path: str)` | 40–64 | html_parser.py | Extract JavaScript functions embedded in HTML. |
| extract_functions | `def extract_functions(self, content: str, file_path: str)` | 54–56 | base.py | Extract function/method definitions. |
| extract_functions | `def extract_functions(self, content: str, file_path: str)` | 38–71 | java_parser.py | Extract Java method definitions. |
| extract_functions | `def extract_functions(self, content: str, file_path: str)` | 42–82 | javascript_parser.py | Extract JavaScript/TypeScript function definiti... |
| extract_functions | `def extract_functions(self, content: str, file_path: str)` | 62–99 | generic_parser.py | Extract function-like patterns. |
| get_language | `def get_language(self)` | 32–34 | base.py | Return the language this parser handles. |
| get_language | `def get_language(self)` | 19–20 | generic_parser.py | – |
| get_language | `def get_language(self)` | 39–40 | python_parser.py | – |
| get_parser | `def get_parser(self, language: str)` | 46–53 | registry.py | Get parser for a specific language. |
| get_version | `def get_version(self)` | 37–39 | base.py | Return parser version for caching purposes. |
| get_version | `def get_version(self)` | 22–23 | generic_parser.py | – |
| get_version | `def get_version(self)` | 42–43 | python_parser.py | – |
| list_supported_languages | `def list_supported_languages(self)` | 55–57 | registry.py | List all supported languages. |
| parse | `def parse(self, content: str, file_path: str)` | 14–29 | base.py | 
        Parse source code content and extract ... |
| parse | `def parse(self, content: str, file_path: str)` | 25–32 | generic_parser.py | Parse source code using generic regex patterns. |
| parse | `def parse(self, content: str, file_path: str)` | 45–50 | python_parser.py | Parse Python source code. |
| register_parser | `def register_parser(self, language: str, parser: BaseParser)` | 59–62 | registry.py | Register a custom parser for a language. |
| validate_content | `def validate_content(self, content: str)` | 41–48 | base.py | 
        Validate that content can be parsed.
 ... |

---

## 🏛️ Classes / Types

| Name | Kind | Inherits / Implements | Lines | File | Doc |
|------|------|-----------------------|-------|---------|-----|
| BaseParser | class | ABC (extends) | 10–95 | base.py | Abstract base class for language-specific parsers. |
| GenericParser | class | BaseParser (extends) | 12–215 | generic_parser.py | Generic parser that uses regex patterns for bas... |
| HTMLParser | class | GenericParser (extends) | 8–127 | html_parser.py | Parser for HTML source code. |
| JavaParser | class | GenericParser (extends) | 8–119 | java_parser.py | Parser for Java source code. |
| JavaScriptParser | class | GenericParser (extends) | 8–129 | javascript_parser.py | Parser for JavaScript and TypeScript source code. |
| ParserRegistry | class | – | 17–62 | registry.py | Registry for managing language-specific parsers. |
| PythonParser | class | BaseParser (extends) | 19–404 | python_parser.py | Parser for Python source code. |
| RustParser | class | GenericParser (extends) | 8–116 | rust_parser.py | Parser for Rust source code. |

---

*Generated by **CBIG** on 2025-08-20 16:37:18 – Repomix-style report.*
