# /Users/cjmacbook/dv/tools/code-extractor/cbig/src/cbig/core – python Overview

---

## 📦 Libraries / Imports

| Library / Package | Version | Source | Language |
|-------------------|---------|--------|-----------|
| cbig.cache.manager | – | pip | python |
| cbig.core.language_detector | – | pip | python |
| cbig.core.models | – | pip | python |
| cbig.core.models | – | pip | python |
| cbig.core.walker | – | pip | python |
| cbig.formatters.markdown | – | pip | python |
| cbig.formatters.structured | – | pip | python |
| cbig.parsers.registry | – | pip | python |
| concurrent.futures | – | pip | python |
| datetime | – | pip | python |
| datetime | – | pip | python |
| logging | – | pip | python |
| logging | – | pip | python |
| logging | – | pip | python |
| os | – | pip | python |
| os | – | pip | python |
| pathlib | – | pip | python |
| pathlib | – | pip | python |
| pathlib | – | pip | python |
| pathlib | – | pip | python |
| pathspec | – | pip | python |
| pydantic | – | pip | python |
| re | – | pip | python |
| shutil | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |
| typing | – | pip | python |

---

## 🔧 Functions / Methods

| Name | Signature | Lines | File | Docstring |
|------|-----------|-------|------|-----------|
| __init__ | `def __init__(self, config: Dict[str, Any])` | 25–51 | processor.py | – |
| __init__ | `def __init__(self, enabled_languages: Optional[List[str]] = None)` | 16–35 | language_detector.py | – |
| __init__ | `def __init__(self, include_patterns: List[str] = None, exclude_patterns: List...` | 15–53 | walker.py | – |
| _build_repo_summary | `def _build_repo_summary(self, file_summaries: Dict[str, FileSummary])` | 156–198 | processor.py | Build repository-level summary from file summar... |
| _build_scopes | `def _build_scopes(self, file_summaries: Dict[str, FileSummary])` | 200–234 | processor.py | Build directory and file scopes from file summa... |
| _detect_c_variant | `def _detect_c_variant(self, file_path: Path)` | 129–155 | language_detector.py | Detect C vs C++ for .h files. |
| _detect_extensionless_file | `def _detect_extensionless_file(self, file_path: Path)` | 157–197 | language_detector.py | Detect language for files without extensions. |
| _detect_js_variant | `def _detect_js_variant(self, file_path: Path)` | 69–102 | language_detector.py | Detect JavaScript variants (.js could be Node, ... |
| _detect_ts_variant | `def _detect_ts_variant(self, file_path: Path)` | 104–127 | language_detector.py | Detect TypeScript variants (.ts vs .tsx). |
| _discover_files | `def _discover_files(self)` | 72–83 | processor.py | Discover and filter files for analysis. |
| _generate_directory_markdown | `def _generate_directory_markdown(self, repo_summary: RepoSummary)` | 257–284 | processor.py | Generate per-directory markdown files. |
| _generate_file_markdown | `def _generate_file_markdown(self, file_summaries: Dict[str, FileSummary])` | 286–295 | processor.py | Generate per-file markdown files. |
| _generate_outputs | `def _generate_outputs(self, repo_summary: RepoSummary, file_summaries: Dict[s...` | 236–249 | processor.py | Generate markdown and structured outputs based ... |
| _generate_repo_markdown | `def _generate_repo_markdown(self, repo_summary: RepoSummary)` | 251–255 | processor.py | Generate repository-level markdown. |
| _get_filename | `def _get_filename(self, name: str, language: str)` | 306–319 | processor.py | Generate filename using template. |
| _get_output_path | `def _get_output_path(self, name: str, language: str)` | 297–304 | processor.py | Get output path for a given name and language. |
| _is_gitignored | `def _is_gitignored(self, relative_path: Path, gitignore_spec: pathspec.PathSpec)` | 190–206 | walker.py | Check if a file is ignored by gitignore patterns. |
| _is_source_file | `def _is_source_file(self, file_path: Path)` | 135–165 | walker.py | Check if a file appears to be source code based... |
| _load_gitignore | `def _load_gitignore(self, root_path: Path)` | 167–188 | walker.py | Load .gitignore patterns if available. |
| _process_files | `def _process_files(self, files: List[Path])` | 85–106 | processor.py | Process files in parallel to extract analysis d... |
| _process_single_file | `def _process_single_file(self, file_path: Path)` | 108–154 | processor.py | Process a single file and extract analysis data. |
| _setup_pathspecs | `def _setup_pathspecs(self)` | 55–65 | walker.py | Setup pathspec matchers for include/exclude pat... |
| _should_exclude_directory | `def _should_exclude_directory(self, dir_path: Path)` | 127–133 | walker.py | Check if a directory should be excluded. |
| _should_include_file | `def _should_include_file(self, file_path: Path, root_path: Path)` | 106–125 | walker.py | Check if a file should be included based on pat... |
| detect_language | `def detect_language(self, file_path: Path)` | 37–67 | language_detector.py | 
        Detect the programming language of a f... |
| get_extensions_for_language | `def get_extensions_for_language(self, language: str)` | 203–206 | language_detector.py | Get file extensions for a given language. |
| get_supported_languages | `def get_supported_languages(self)` | 199–201 | language_detector.py | Get list of supported languages. |
| process | `def process(self)` | 53–70 | processor.py | Process the repository and generate analysis re... |
| walk | `def walk(self, root_path: Path)` | 67–104 | walker.py | 
        Walk the directory tree starting from ... |

---

## 🏛️ Classes / Types

| Name | Kind | Inherits / Implements | Lines | File | Doc |
|------|------|-----------------------|-------|---------|-----|
| CBIGProcessor | class | – | 22–319 | processor.py | Main processor that coordinates the analysis pi... |
| Class | class | BaseModel (extends) | 32–42 | models.py | Represents a class, struct, or type. |
| Comment | class | BaseModel (extends) | 45–51 | models.py | Represents a top-level comment block. |
| Dependency | class | BaseModel (extends) | 9–16 | models.py | Represents a library/package dependency. |
| DirectorySummary | class | BaseModel (extends) | 65–74 | models.py | Summary data for a directory. |
| FileSummary | class | BaseModel (extends) | 54–62 | models.py | Summary data for a single file. |
| FileWalker | class | – | 12–206 | walker.py | Walks directory trees to discover source files ... |
| Function | class | BaseModel (extends) | 19–29 | models.py | Represents a function or method. |
| LanguageConfig | class | BaseModel (extends) | 90–96 | models.py | Configuration for a specific language parser. |
| LanguageDetector | class | – | 13–206 | language_detector.py | Detects programming language of source files. |
| RepoSummary | class | BaseModel (extends) | 77–87 | models.py | Complete repository analysis result. |

---

*Generated by **CBIG** on 2025-08-20 16:37:18 – Repomix-style report.*
