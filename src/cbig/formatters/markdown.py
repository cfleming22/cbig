"""Markdown formatter for generating Repomix-style output."""

from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import logging

from cbig.core.models import RepoSummary, DirectorySummary, FileSummary

logger = logging.getLogger(__name__)


class MarkdownFormatter:
    """Formats analysis results as Repomix-style markdown."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.sections = config.get("sections", {})
    
    def generate_repo_markdown(self, repo_summary: RepoSummary, output_path: Path):
        """Generate repository-level markdown file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            # Header
            repo_name = Path(repo_summary.root).name
            f.write(f"# {repo_name} – Repository Overview\n\n")
            f.write("---\n\n")
            
            # Summary section
            if self.sections.get("summary", True):
                self._write_summary_section(f, repo_summary)
            
            # Dependencies section
            if self.sections.get("deps", True):
                self._write_dependencies_section(f, repo_summary.dependencies)
            
            # Functions section
            if self.sections.get("functions", True):
                self._write_functions_section(f, repo_summary.functions)
            
            # Classes section
            if self.sections.get("classes", True):
                self._write_classes_section(f, repo_summary.classes)
            
            # Comments section
            if self.sections.get("comments", False):
                self._write_comments_section(f, repo_summary.comments)
            
            # Footer
            self._write_footer(f, repo_summary.generated_at)
    
    def generate_directory_markdown(self, dir_summary: DirectorySummary, output_path: Path):
        """Generate directory-level markdown file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            # Header
            dir_name = dir_summary.directory
            if dir_name == "root":
                dir_name = "."
            languages = " + ".join(dir_summary.languages) if dir_summary.languages else "Mixed"
            f.write(f"# {dir_name} – {languages} Overview\n\n")
            f.write("---\n\n")
            
            # File list
            if dir_summary.files:
                f.write("## 📁 Files in Directory\n\n")
                for file_path in sorted(dir_summary.files):
                    f.write(f"- {file_path}\n")
                f.write("\n---\n\n")
            
            # Dependencies section
            if self.sections.get("deps", True):
                self._write_dependencies_section(f, dir_summary.dependencies)
            
            # Functions section
            if self.sections.get("functions", True):
                self._write_functions_section(f, dir_summary.functions)
            
            # Classes section
            if self.sections.get("classes", True):
                self._write_classes_section(f, dir_summary.classes)
            
            # Comments section
            if self.sections.get("comments", False):
                self._write_comments_section(f, dir_summary.comments)
            
            # Footer
            self._write_footer(f, datetime.now())
    
    def generate_file_markdown(self, file_summary: FileSummary, output_path: Path):
        """Generate file-level markdown file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            # Header
            file_name = Path(file_summary.file_path).name
            language = file_summary.language.title()
            f.write(f"# {file_name} – {language} Overview\n\n")
            f.write("---\n\n")
            
            # File info
            f.write("## 📄 File Information\n\n")
            f.write(f"- **File**: {file_summary.file_path}\n")
            f.write(f"- **Language**: {file_summary.language}\n")
            f.write(f"- **Lines of Code**: {file_summary.loc}\n")
            f.write("\n---\n\n")
            
            # Dependencies section
            if self.sections.get("deps", True):
                self._write_dependencies_section(f, file_summary.dependencies)
            
            # Functions section
            if self.sections.get("functions", True):
                self._write_functions_section(f, file_summary.functions)
            
            # Classes section
            if self.sections.get("classes", True):
                self._write_classes_section(f, file_summary.classes)
            
            # Comments section
            if self.sections.get("comments", False):
                self._write_comments_section(f, file_summary.comments)
            
            # Footer
            self._write_footer(f, datetime.now())
    
    def _write_summary_section(self, f, repo_summary: RepoSummary):
        """Write repository summary section."""
        f.write("## 📊 Repository Summary\n\n")
        
        summary = repo_summary.summary
        f.write(f"- **Total Files**: {summary.get('total_files', 0)}\n")
        f.write(f"- **Total Lines of Code**: {summary.get('total_loc', 0):,}\n")
        f.write(f"- **Languages**: {', '.join(repo_summary.languages)}\n")
        
        # Per-language breakdown
        per_lang = summary.get('per_language', {})
        if per_lang:
            f.write("\n### Language Breakdown\n\n")
            f.write("| Language | Files | Lines of Code |\n")
            f.write("|----------|-------|---------------|\n")
            for lang, stats in sorted(per_lang.items()):
                files = stats.get('files', 0)
                loc = stats.get('loc', 0)
                f.write(f"| {lang.title()} | {files} | {loc:,} |\n")
        
        f.write("\n---\n\n")
    
    def _write_dependencies_section(self, f, dependencies: List):
        """Write dependencies section."""
        f.write("## 📦 Libraries / Imports\n\n")
        
        if not dependencies:
            f.write("*No dependencies found.*\n\n")
            f.write("---\n\n")
            return
        
        # Group by source
        by_source = {}
        for dep in dependencies:
            source = dep.source or "unknown"
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(dep)
        
        f.write("| Library / Package | Version | Source | Language |\n")
        f.write("|-------------------|---------|--------|-----------|\n")
        
        # Sort dependencies
        sort_field = self.config.get("sort_options", {}).get("deps", "name")
        for source, deps in sorted(by_source.items()):
            sorted_deps = sorted(deps, key=lambda x: getattr(x, sort_field, x.name))
            for dep in sorted_deps:
                version = dep.version or "–"
                f.write(f"| {dep.name} | {version} | {dep.source or '–'} | {dep.language} |\n")
        
        f.write("\n---\n\n")
    
    def _write_functions_section(self, f, functions: List):
        """Write functions section."""
        f.write("## 🔧 Functions / Methods\n\n")
        
        if not functions:
            f.write("*No functions found.*\n\n")
            f.write("---\n\n")
            return
        
        f.write("| Name | Signature | Lines | File | Docstring |\n")
        f.write("|------|-----------|-------|------|-----------|\n")
        
        # Sort functions
        sort_field = self.config.get("sort_options", {}).get("functions", "name")
        sorted_functions = sorted(functions, key=lambda x: getattr(x, sort_field, x.name))
        
        for func in sorted_functions:
            # Truncate signature for display
            signature = func.signature
            if len(signature) > 80:
                signature = signature[:77] + "..."
            
            # Format line range
            line_range = f"{func.line_start}"
            if func.line_end != func.line_start:
                line_range = f"{func.line_start}–{func.line_end}"
            
            # File name (just the filename, not full path)
            file_name = Path(func.file).name if func.file else "–"
            
            # Docstring (truncated)
            docstring = func.docstring or "–"
            if len(docstring) > 50:
                docstring = docstring[:47] + "..."
            
            f.write(f"| {func.name} | `{signature}` | {line_range} | {file_name} | {docstring} |\n")
        
        f.write("\n---\n\n")
    
    def _write_classes_section(self, f, classes: List):
        """Write classes section."""
        f.write("## 🏛️ Classes / Types\n\n")
        
        if not classes:
            f.write("*No classes found.*\n\n")
            f.write("---\n\n")
            return
        
        f.write("| Name | Kind | Inherits / Implements | Lines | File | Doc |\n")
        f.write("|------|------|-----------------------|-------|---------|-----|\n")
        
        # Sort classes
        sort_field = self.config.get("sort_options", {}).get("classes", "name")
        sorted_classes = sorted(classes, key=lambda x: getattr(x, sort_field, x.name))
        
        for cls in sorted_classes:
            # Format inheritance info
            inheritance = []
            if cls.inherits:
                inheritance.append(f"{cls.inherits} (extends)")
            if cls.implements:
                for impl in cls.implements:
                    inheritance.append(f"{impl} (implements)")
            
            inheritance_str = ", ".join(inheritance) if inheritance else "–"
            if len(inheritance_str) > 40:
                inheritance_str = inheritance_str[:37] + "..."
            
            # Format line range
            line_range = f"{cls.line_start}"
            if cls.line_end != cls.line_start:
                line_range = f"{cls.line_start}–{cls.line_end}"
            
            # File name
            file_name = Path(cls.file).name if cls.file else "–"
            
            # Doc (truncated)
            doc = cls.doc or "–"
            if len(doc) > 50:
                doc = doc[:47] + "..."
            
            f.write(f"| {cls.name} | {cls.kind} | {inheritance_str} | {line_range} | {file_name} | {doc} |\n")
        
        f.write("\n---\n\n")
    
    def _write_comments_section(self, f, comments: List):
        """Write comments section."""
        f.write("## 💬 Top-Level Comments\n\n")
        
        if not comments:
            f.write("*No comments found.*\n\n")
            f.write("---\n\n")
            return
        
        # Group comments by file
        by_file = {}
        for comment in comments:
            file_name = Path(comment.file).name if comment.file else "unknown"
            if file_name not in by_file:
                by_file[file_name] = []
            by_file[file_name].append(comment)
        
        for file_name, file_comments in sorted(by_file.items()):
            f.write(f"### {file_name}\n\n")
            for comment in file_comments:
                # Format comment text with proper quoting
                text_lines = comment.text.strip().split('\n')
                for line in text_lines:
                    f.write(f"> {line}\n")
                f.write(f">\n> *Lines {comment.line_start}–{comment.line_end}*\n\n")
        
        f.write("---\n\n")
    
    def _write_footer(self, f, generated_at: datetime):
        """Write footer with generation info."""
        timestamp = generated_at.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"*Generated by **CBIG** on {timestamp} – Repomix-style report.*\n")