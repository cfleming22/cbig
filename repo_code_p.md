# src – Repository Overview

---

## 📊 Repository Summary

- **Total Files**: 22
- **Total Lines of Code**: 2,587
- **Languages**: python

### Language Breakdown

| Language | Files | Lines of Code |
|----------|-------|---------------|
| Python | 22 | 2,587 |

---

## 📦 Libraries / Imports

| Library / Package | Version | Source | Language |
|-------------------|---------|--------|-----------|
| abc | – | pip | python |
| cbig.cache.manager | – | pip | python |
| cbig.core.language_detector | – | pip | python |
| cbig.core.models | – | pip | python |
| cbig.core.models | – | pip | python |
| cbig.core.models | – | pip | python |
| cbig.core.models | – | pip | python |
| cbig.core.models | – | pip | python |
| cbig.core.models | – | pip | python |
| cbig.core.processor | – | pip | python |
| cbig.core.walker | – | pip | python |
| cbig.formatters.markdown | – | pip | python |
| cbig.formatters.structured | – | pip | python |
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
| cbig.parsers.registry | – | pip | python |
| cbig.parsers.rust_parser | – | pip | python |
| concurrent.futures | – | pip | python |
| datetime | – | pip | python |
| datetime | – | pip | python |
| datetime | – | pip | python |
| hashlib | – | pip | python |
| json | – | pip | python |
| json | – | pip | python |
| logging | – | pip | python |
| logging | – | pip | python |
| logging | – | pip | python |
| logging | – | pip | python |
| logging | – | pip | python |
| logging | – | pip | python |
| logging | – | pip | python |
| logging | – | pip | python |
| logging | – | pip | python |
| logging | – | pip | python |
| logging | – | pip | python |
| mpor | – | pip | python |
| os | – | pip | python |
| os | – | pip | python |
| os | – | pip | python |
| os | – | pip | python |
| pathlib | – | pip | python |
| pathlib | – | pip | python |
| pathlib | – | pip | python |
| pathlib | – | pip | python |
| pathlib | – | pip | python |
| pathlib | – | pip | python |
| pathlib | – | pip | python |
| pathlib | – | pip | python |
| pathspec | – | pip | python |
| pickle | – | pip | python |
| pydantic | – | pip | python |
| re | – | pip | python |
| re | – | pip | python |
| re | – | pip | python |
| re | – | pip | python |
| re | – | pip | python |
| re | – | pip | python |
| re | – | pip | python |
| rich.console | – | pip | python |
| rich.logging | – | pip | python |
| shutil | – | pip | python |
| sys | – | pip | python |
| tree_sitter | – | pip | python |
| typer | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| yaml | – | pip | python |

---

## 🔧 Functions / Methods

| Name | Signature | Lines | File | Docstring |
|------|-----------|-------|------|-----------|
|        """Wri | `def        """Write footer with generation info.""` | 288–291 | markdown.py | timestamp = generated_at.strftime("%Y-%m |
|  classes: List):
      | `def  classes: List):
        """Write classes sect` | 214–258 | markdown.py |       f.write("## 🏛️ Classes |
| __init__ | `def __init__(self)` | 11–12 | rust_parser.py | – |
| __init__ | `def __init__(self)` | 11–12 | html_parser.py | – |
| __init__ | `def __init__(self)` | 22–37 | python_parser.py | – |
| __init__ | `def __init__(self)` | 11–12 | javascript_parser.py | – |
| __init__ | `def __init__(self)` | 11–12 | java_parser.py | – |
| __init__ | `def __init__(self)` | 20–22 | registry.py | – |
| __init__ | `def __init__(self, language: str = "generic")` | 15–17 | generic_parser.py | – |
| __init__ | `def __init__(self, include_patterns: List[str] = None, exclude_patterns: List...` | 15–53 | walker.py | – |
| __init__ | `def __init__(self, config: Dict[str, Any])` | 16–18 | markdown.py | – |
| __init__ | `def __init__(self, enabled_languages: Optional[List[str]] = None)` | 16–35 | language_detector.py | – |
| __init__ | `def __init__(self, cache_dir: Path)` | 19–27 | manager.py | – |
| __init__ | `def __init__(self, config: Dict[str, Any])` | 17–19 | structured.py | – |
| __init__ | `def __init__(self, config: Dict[str, Any])` | 25–51 | processor.py | – |
| _build_repo_summary | `def _build_repo_summary(self, file_summaries: Dict[str, FileSummary])` | 156–198 | processor.py | Build repository-level summary from file summar... |
| _build_scopes | `def _build_scopes(self, file_summaries: Dict[str, FileSummary])` | 200–234 | processor.py | Build directory and file scopes from file summa... |
| _convert_to_dict | `def _convert_to_dict(self, repo_summary: RepoSummary)` | 35–110 | structured.py | Convert RepoSummary to dictionary for serializa... |
| _detect_c_variant | `def _detect_c_variant(self, file_path: Path)` | 129–155 | language_detector.py | Detect C vs C++ for .h files. |
| _detect_extensionless_file | `def _detect_extensionless_file(self, file_path: Path)` | 157–197 | language_detector.py | Detect language for files without extensions. |
| _detect_js_variant | `def _detect_js_variant(self, file_path: Path)` | 69–102 | language_detector.py | Detect JavaScript variants (.js could be Node, ... |
| _detect_ts_variant | `def _detect_ts_variant(self, file_path: Path)` | 104–127 | language_detector.py | Detect TypeScript variants (.ts vs .tsx). |
| _discover_files | `def _discover_files(self)` | 72–83 | processor.py | Discover and filter files for analysis. |
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
| _generate_directory_markdown | `def _generate_directory_markdown(self, repo_summary: RepoSummary)` | 257–284 | processor.py | Generate per-directory markdown files. |
| _generate_file_markdown | `def _generate_file_markdown(self, file_summaries: Dict[str, FileSummary])` | 286–295 | processor.py | Generate per-file markdown files. |
| _generate_outputs | `def _generate_outputs(self, repo_summary: RepoSummary, file_summaries: Dict[s...` | 236–249 | processor.py | Generate markdown and structured outputs based ... |
| _generate_repo_markdown | `def _generate_repo_markdown(self, repo_summary: RepoSummary)` | 251–255 | processor.py | Generate repository-level markdown. |
| _get_cache_file_path | `def _get_cache_file_path(self, cache_key: str)` | 67–73 | manager.py | Get the cache file path for a given cache key. |
| _get_cache_key | `def _get_cache_key(self, file_path: Path)` | 61–65 | manager.py | Generate cache key for a file. |
| _get_file_hash | `def _get_file_hash(self, file_path: Path)` | 51–59 | manager.py | Calculate SHA-256 hash of file content. |
| _get_filename | `def _get_filename(self, name: str, language: str)` | 306–319 | processor.py | Generate filename using template. |
| _get_output_path | `def _get_output_path(self, name: str, language: str)` | 297–304 | processor.py | Get output path for a given name and language. |
| _initialize_parsers | `def _initialize_parsers(self)` | 24–44 | registry.py | Initialize all available parsers. |
| _is_gitignored | `def _is_gitignored(self, relative_path: Path, gitignore_spec: pathspec.PathSpec)` | 190–206 | walker.py | Check if a file is ignored by gitignore patterns. |
| _is_source_file | `def _is_source_file(self, file_path: Path)` | 135–165 | walker.py | Check if a file appears to be source code based... |
| _load_gitignore | `def _load_gitignore(self, root_path: Path)` | 167–188 | walker.py | Load .gitignore patterns if available. |
| _load_metadata | `def _load_metadata(self)` | 29–41 | manager.py | Load cache metadata. |
| _parse_with_regex | `def _parse_with_regex(self, content: str, file_path: str)` | 260–267 | python_parser.py | Fallback regex-based parsing when Tree-sitter i... |
| _parse_with_tree_sitter | `def _parse_with_tree_sitter(self, content: str, file_path: str)` | 52–66 | python_parser.py | Parse using Tree-sitter for accurate AST parsing. |
| _process_files | `def _process_files(self, files: List[Path])` | 85–106 | processor.py | Process files in parallel to extract analysis d... |
| _process_single_file | `def _process_single_file(self, file_path: Path)` | 108–154 | processor.py | Process a single file and extract analysis data. |
| _safe_parse | `def _safe_parse(self, content: str, file_path: str)` | 66–86 | base.py | 
        Safely parse content with error handli... |
| _save_comment_block | `def _save_comment_block(self, comments: List, block: List[str], start: int, e...` | 205–215 | generic_parser.py | Save a comment block to the results. |
| _save_metadata | `def _save_metadata(self)` | 43–49 | manager.py | Save cache metadata. |
| _setup_pathspecs | `def _setup_pathspecs(self)` | 55–65 | walker.py | Setup pathspec matchers for include/exclude pat... |
| _should_exclude_directory | `def _should_exclude_directory(self, dir_path: Path)` | 127–133 | walker.py | Check if a directory should be excluded. |
| _should_include_file | `def _should_include_file(self, file_path: Path, root_path: Path)` | 106–125 | walker.py | Check if a file should be included based on pat... |
| _write_json | `def _write_json(self, data: Dict[str, Any], output_path: Optional[str])` | 112–121 | structured.py | Write data as JSON. |
| _write_text | `def _write_text(self, data: Dict[str, Any], output_path: Optional[str])` | 134–212 | structured.py | Write data as plain text summary. |
| _write_yaml | `def _write_yaml(self, data: Dict[str, Any], output_path: Optional[str])` | 123–132 | structured.py | Write data as YAML. |
| cies_section(self, f, depen | `def cies_section(self, f, dependencies: List):
        """Wr` | 145–173 | markdown.py | encies section."""
        f.writ |
| cleanup_orphaned | `def cleanup_orphaned(self)` | 185–209 | manager.py | Remove orphaned cache files that are no longer ... |
| clear | `def clear(self)` | 142–159 | manager.py | Clear all cache entries. |
| detect_language | `def detect_language(self, file_path: Path)` | 37–67 | language_detector.py | 
        Detect the programming language of a f... |
| e_file_markdown(self,  | `def e_file_markdown(self, file_summary: FileSummary, output_path: Path):
     ` | 88–121 | markdown.py | rate file-level markdown file."""
       |
| extract_classes | `def extract_classes(self, content: str, file_path: str)` | 74–116 | rust_parser.py | Extract Rust struct, enum, and trait definitions. |
| extract_classes | `def extract_classes(self, content: str, file_path: str)` | 101–127 | html_parser.py | Extract HTML elements as 'classes' (custom elem... |
| extract_classes | `def extract_classes(self, content: str, file_path: str)` | 84–129 | javascript_parser.py | Extract JavaScript/TypeScript class definitions. |
| extract_classes | `def extract_classes(self, content: str, file_path: str)` | 73–119 | java_parser.py | Extract Java class definitions. |
| extract_classes | `def extract_classes(self, content: str, file_path: str)` | 101–144 | generic_parser.py | Extract class-like patterns. |
| extract_classes | `def extract_classes(self, content: str, file_path: str)` | 58–60 | base.py | Extract class/type definitions. |
| extract_comments | `def extract_comments(self, content: str, file_path: str)` | 146–203 | generic_parser.py | Extract comment blocks. |
| extract_comments | `def extract_comments(self, content: str, file_path: str)` | 62–64 | base.py | Extract top-level comments. |
| extract_dependencies | `def extract_dependencies(self, content: str, file_path: str)` | 14–38 | rust_parser.py | Extract Rust use statements and external crates. |
| extract_dependencies | `def extract_dependencies(self, content: str, file_path: str)` | 14–38 | html_parser.py | Extract HTML dependencies (scripts, stylesheets... |
| extract_dependencies | `def extract_dependencies(self, content: str, file_path: str)` | 14–40 | javascript_parser.py | Extract JavaScript/TypeScript import statements. |
| extract_dependencies | `def extract_dependencies(self, content: str, file_path: str)` | 14–36 | java_parser.py | Extract Java import statements. |
| extract_dependencies | `def extract_dependencies(self, content: str, file_path: str)` | 34–60 | generic_parser.py | Extract import-like patterns. |
| extract_dependencies | `def extract_dependencies(self, content: str, file_path: str)` | 50–52 | base.py | Extract import/dependency information. |
| extract_functions | `def extract_functions(self, content: str, file_path: str)` | 40–72 | rust_parser.py | Extract Rust function definitions. |
| extract_functions | `def extract_functions(self, content: str, file_path: str)` | 40–64 | html_parser.py | Extract JavaScript functions embedded in HTML. |
| extract_functions | `def extract_functions(self, content: str, file_path: str)` | 42–82 | javascript_parser.py | Extract JavaScript/TypeScript function definiti... |
| extract_functions | `def extract_functions(self, content: str, file_path: str)` | 38–71 | java_parser.py | Extract Java method definitions. |
| extract_functions | `def extract_functions(self, content: str, file_path: str)` | 62–99 | generic_parser.py | Extract function-like patterns. |
| extract_functions | `def extract_functions(self, content: str, file_path: str)` | 54–56 | base.py | Extract function/method definitions. |
| generate | `def generate(self, repo_summary: RepoSummary, output_path: Optional[str] = None)` | 21–33 | structured.py | Generate structured output in the specified for... |
| generate_repo_markdown | `def generate_repo_markdown(self, repo_summary: RepoSummary, output_path: Path)` | 20–49 | markdown.py | Generate repository-level markdown file. |
| ges():
   | `def ges():
    ` | 255–264 | main.py | t supported languages and their configurations.... |
| get | `def get(self, file_path: Path)` | 75–113 | manager.py | 
        Retrieve cached result for a file.
   ... |
| get_extensions_for_language | `def get_extensions_for_language(self, language: str)` | 203–206 | language_detector.py | Get file extensions for a given language. |
| get_language | `def get_language(self)` | 39–40 | python_parser.py | – |
| get_language | `def get_language(self)` | 19–20 | generic_parser.py | – |
| get_language | `def get_language(self)` | 32–34 | base.py | Return the language this parser handles. |
| get_parser | `def get_parser(self, language: str)` | 46–53 | registry.py | Get parser for a specific language. |
| get_stats | `def get_stats(self)` | 161–183 | manager.py | Get cache statistics. |
| get_supported_languages | `def get_supported_languages(self)` | 199–201 | language_detector.py | Get list of supported languages. |
| get_version | `def get_version(self)` | 42–43 | python_parser.py | – |
| get_version | `def get_version(self)` | 22–23 | generic_parser.py | – |
| get_version | `def get_version(self)` | 37–39 | base.py | Return parser version for caching purposes. |
| ist):
        """Write  | `def ist):
        """Write comments section."""
    ` | 260–286 | markdown.py | e("## 💬 Top-Level Comments\n\ |
| list_supported_languages | `def list_supported_languages(self)` | 55–57 | registry.py | List all supported languages. |
| main | `def main(
    path: str = typer.Option(
        ".",
        "--path", "-p",
...` | 41–244 | main.py | 
    Generate directory-level code insights wit... |
| n():
   | `def n():
    ` | 248–251 | main.py | w version information."""
    f |
| nerate_directory_markdown(s | `def nerate_directory_markdown(self, dir_summary: DirectorySummary, output_pat...` | 51–86 | markdown.py | Generate directory-level markdown file."""
  |
| on(self, f, functions: L | `def on(self, f, functions: List):
        """Write fun` | 175–212 | markdown.py | tion."""
        f.write("## 🔧 |
| parse | `def parse(self, content: str, file_path: str)` | 45–50 | python_parser.py | Parse Python source code. |
| parse | `def parse(self, content: str, file_path: str)` | 25–32 | generic_parser.py | Parse source code using generic regex patterns. |
| parse | `def parse(self, content: str, file_path: str)` | 14–29 | base.py | 
        Parse source code content and extract ... |
| process | `def process(self)` | 53–70 | processor.py | Process the repository and generate analysis re... |
| put | `def put(self, file_path: Path, result: FileSummary)` | 115–140 | manager.py | Store result in cache. |
| register_parser | `def register_parser(self, language: str, parser: BaseParser)` | 59–62 | registry.py | Register a custom parser for a language. |
| ry_section(self, f, re | `def ry_section(self, f, repo_summary: RepoSummary):
        ""` | 123–143 | markdown.py | ository summary section."""
        f.w |
| setup_logging | `def setup_logging(verbose: bool = False, quiet: bool = False)` | 24–37 | main.py | Setup logging configuration. |
| validate_content | `def validate_content(self, content: str)` | 41–48 | base.py | 
        Validate that content can be parsed.
 ... |
| walk | `def walk(self, root_path: Path)` | 67–104 | walker.py | 
        Walk the directory tree starting from ... |

---

## 🏛️ Classes / Types

| Name | Kind | Inherits / Implements | Lines | File | Doc |
|------|------|-----------------------|-------|---------|-----|
| BaseParser | class | ABC (extends) | 10–95 | base.py | Abstract base class for language-specific parsers. |
| CBIGProcessor | class | – | 22–319 | processor.py | Main processor that coordinates the analysis pi... |
| CacheManager | class | – | 16–209 | manager.py | Manages caching of parsed file results to avoid... |
| Class | class | BaseModel (extends) | 32–42 | models.py | Represents a class, struct, or type. |
| Comment | class | BaseModel (extends) | 45–51 | models.py | Represents a top-level comment block. |
| Dependency | class | BaseModel (extends) | 9–16 | models.py | Represents a library/package dependency. |
| DirectorySummary | class | BaseModel (extends) | 65–74 | models.py | Summary data for a directory. |
| FileSummary | class | BaseModel (extends) | 54–62 | models.py | Summary data for a single file. |
| FileWalker | class | – | 12–206 | walker.py | Walks directory trees to discover source files ... |
| Function | class | BaseModel (extends) | 19–29 | models.py | Represents a function or method. |
| GenericParser | class | BaseParser (extends) | 12–215 | generic_parser.py | Generic parser that uses regex patterns for bas... |
| HTMLParser | class | GenericParser (extends) | 8–127 | html_parser.py | Parser for HTML source code. |
| JavaParser | class | GenericParser (extends) | 8–119 | java_parser.py | Parser for Java source code. |
| JavaScriptParser | class | GenericParser (extends) | 8–129 | javascript_parser.py | Parser for JavaScript and TypeScript source code. |
| LanguageConfig | class | BaseModel (extends) | 90–96 | models.py | Configuration for a specific language parser. |
| LanguageDetector | class | – | 13–206 | language_detector.py | Detects programming language of source files. |
| MarkdownFormatter | class | – | 13–291 | markdown.py | Formats analysis results as Repomix-style markd... |
| ParserRegistry | class | – | 17–62 | registry.py | Registry for managing language-specific parsers. |
| PythonParser | class | BaseParser (extends) | 19–404 | python_parser.py | Parser for Python source code. |
| RepoSummary | class | BaseModel (extends) | 77–87 | models.py | Complete repository analysis result. |
| RustParser | class | GenericParser (extends) | 8–116 | rust_parser.py | Parser for Rust source code. |
| StructuredFormatter | class | – | 14–212 | structured.py | Formats analysis results as structured data (JS... |

---

*Generated by **CBIG** on 2025-08-20 16:37:00 – Repomix-style report.*
