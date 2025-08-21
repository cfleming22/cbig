"""Structured formatters for JSON, YAML, and other formats."""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging

from cbig.core.models import RepoSummary

logger = logging.getLogger(__name__)


class StructuredFormatter:
    """Formats analysis results as structured data (JSON, YAML, etc.)."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.format = config.get("format", "json")
    
    def generate(self, repo_summary: RepoSummary, output_path: Optional[str] = None):
        """Generate structured output in the specified format."""
        # Convert to dictionary for serialization
        data = self._convert_to_dict(repo_summary)
        
        if self.format == "json":
            self._write_json(data, output_path)
        elif self.format == "yaml":
            self._write_yaml(data, output_path)
        elif self.format == "txt":
            self._write_text(data, output_path)
        else:
            logger.warning(f"Unsupported format: {self.format}")
    
    def _convert_to_dict(self, repo_summary: RepoSummary) -> Dict[str, Any]:
        """Convert RepoSummary to dictionary for serialization."""
        data = {
            "repo": {
                "root": repo_summary.root,
                "languages": repo_summary.languages,
                "summary": repo_summary.summary,
                "generated_at": repo_summary.generated_at.isoformat()
            }
        }
        
        # Add sections based on configuration
        sections = self.config.get("sections", {})
        
        if sections.get("deps", True):
            data["dependencies"] = [
                {
                    "language": dep.language,
                    "name": dep.name,
                    "version": dep.version,
                    "source": dep.source,
                    "group": dep.group,
                    "artifact": dep.artifact
                }
                for dep in repo_summary.dependencies
            ]
        
        if sections.get("functions", True):
            data["functions"] = [
                {
                    "language": func.language,
                    "file": func.file,
                    "name": func.name,
                    "signature": func.signature,
                    "line_start": func.line_start,
                    "line_end": func.line_end,
                    "docstring": func.docstring,
                    "is_method": func.is_method,
                    "class_name": func.class_name
                }
                for func in repo_summary.functions
            ]
        
        if sections.get("classes", True):
            data["classes"] = [
                {
                    "language": cls.language,
                    "file": cls.file,
                    "name": cls.name,
                    "kind": cls.kind,
                    "inherits": cls.inherits,
                    "implements": cls.implements,
                    "line_start": cls.line_start,
                    "line_end": cls.line_end,
                    "doc": cls.doc
                }
                for cls in repo_summary.classes
            ]
        
        if sections.get("comments", False):
            data["comments"] = [
                {
                    "language": comment.language,
                    "file": comment.file,
                    "line_start": comment.line_start,
                    "line_end": comment.line_end,
                    "text": comment.text
                }
                for comment in repo_summary.comments
            ]
        
        # Add scopes if requested
        if self.config.get("include_scopes", False):
            data["scopes"] = repo_summary.scopes
        
        return data
    
    def _write_json(self, data: Dict[str, Any], output_path: Optional[str]):
        """Write data as JSON."""
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_str)
            logger.info(f"Generated JSON output: {output_path}")
        else:
            print(json_str)
    
    def _write_yaml(self, data: Dict[str, Any], output_path: Optional[str]):
        """Write data as YAML."""
        yaml_str = yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(yaml_str)
            logger.info(f"Generated YAML output: {output_path}")
        else:
            print(yaml_str)
    
    def _write_text(self, data: Dict[str, Any], output_path: Optional[str]):
        """Write data as plain text summary."""
        lines = []
        
        # Repository info
        repo = data.get("repo", {})
        lines.append(f"Repository: {repo.get('root', 'Unknown')}")
        lines.append(f"Languages: {', '.join(repo.get('languages', []))}")
        lines.append(f"Generated: {repo.get('generated_at', 'Unknown')}")
        lines.append("")
        
        # Summary
        summary = repo.get("summary", {})
        lines.append("Summary:")
        lines.append(f"  Total Files: {summary.get('total_files', 0)}")
        lines.append(f"  Total LOC: {summary.get('total_loc', 0):,}")
        
        per_lang = summary.get("per_language", {})
        if per_lang:
            lines.append("  Per Language:")
            for lang, stats in sorted(per_lang.items()):
                files = stats.get('files', 0)
                loc = stats.get('loc', 0)
                lines.append(f"    {lang}: {files} files, {loc:,} LOC")
        lines.append("")
        
        # Dependencies
        deps = data.get("dependencies", [])
        if deps:
            lines.append(f"Dependencies ({len(deps)}):")
            by_lang = {}
            for dep in deps:
                lang = dep.get("language", "unknown")
                if lang not in by_lang:
                    by_lang[lang] = []
                by_lang[lang].append(dep["name"])
            
            for lang, dep_names in sorted(by_lang.items()):
                lines.append(f"  {lang}: {', '.join(sorted(set(dep_names)))}")
            lines.append("")
        
        # Functions
        functions = data.get("functions", [])
        if functions:
            lines.append(f"Functions ({len(functions)}):")
            by_lang = {}
            for func in functions:
                lang = func.get("language", "unknown")
                if lang not in by_lang:
                    by_lang[lang] = 0
                by_lang[lang] += 1
            
            for lang, count in sorted(by_lang.items()):
                lines.append(f"  {lang}: {count}")
            lines.append("")
        
        # Classes
        classes = data.get("classes", [])
        if classes:
            lines.append(f"Classes ({len(classes)}):")
            by_lang = {}
            for cls in classes:
                lang = cls.get("language", "unknown")
                if lang not in by_lang:
                    by_lang[lang] = 0
                by_lang[lang] += 1
            
            for lang, count in sorted(by_lang.items()):
                lines.append(f"  {lang}: {count}")
            lines.append("")
        
        text_output = '\n'.join(lines)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text_output)
            logger.info(f"Generated text output: {output_path}")
        else:
            print(text_output)