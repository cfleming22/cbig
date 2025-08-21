"""Main processor that orchestrates the CBIG analysis pipeline."""

import logging
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from cbig.core.models import RepoSummary, DirectorySummary, FileSummary, LANGUAGE_CONFIGS
from cbig.core.walker import FileWalker
from cbig.core.language_detector import LanguageDetector
from cbig.parsers.registry import ParserRegistry
from cbig.formatters.markdown import MarkdownFormatter
from cbig.formatters.structured import StructuredFormatter
from cbig.cache.manager import CacheManager

logger = logging.getLogger(__name__)


class CBIGProcessor:
    """Main processor that coordinates the analysis pipeline."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.root_path = Path(config["path"]).resolve()
        
        # Initialize components
        self.walker = FileWalker(
            include_patterns=config.get("include", []),
            exclude_patterns=config.get("exclude", [])
        )
        self.language_detector = LanguageDetector(
            enabled_languages=config.get("languages")
        )
        self.parser_registry = ParserRegistry()
        
        # Initialize cache if enabled
        self.cache_manager = None
        if config.get("cache_dir"):
            cache_path = Path(config["cache_dir"])
            if config.get("clear_cache") and cache_path.exists():
                shutil.rmtree(cache_path)
            self.cache_manager = CacheManager(cache_path)
        
        # Initialize formatters
        self.markdown_formatter = MarkdownFormatter(config)
        self.structured_formatter = StructuredFormatter(config)
        
        self.max_workers = config.get("max_workers", os.cpu_count())
    
    def process(self) -> RepoSummary:
        """Process the repository and generate analysis results."""
        logger.info(f"Starting analysis of {self.root_path}")
        
        # Walk files and detect languages
        files = self._discover_files()
        logger.info(f"Found {len(files)} files to analyze")
        
        # Process files in parallel
        file_summaries = self._process_files(files)
        
        # Build repository summary
        repo_summary = self._build_repo_summary(file_summaries)
        
        # Generate outputs
        self._generate_outputs(repo_summary, file_summaries)
        
        return repo_summary
    
    def _discover_files(self) -> List[Path]:
        """Discover and filter files for analysis."""
        all_files = list(self.walker.walk(self.root_path))
        
        # Filter by language
        filtered_files = []
        for file_path in all_files:
            language = self.language_detector.detect_language(file_path)
            if language:
                filtered_files.append(file_path)
        
        return filtered_files
    
    def _process_files(self, files: List[Path]) -> Dict[str, FileSummary]:
        """Process files in parallel to extract analysis data."""
        file_summaries = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit tasks
            future_to_file = {
                executor.submit(self._process_single_file, file_path): file_path
                for file_path in files
            }
            
            # Collect results
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    summary = future.result()
                    if summary:
                        file_summaries[str(file_path)] = summary
                except Exception as e:
                    logger.warning(f"Failed to process {file_path}: {e}")
        
        return file_summaries
    
    def _process_single_file(self, file_path: Path) -> Optional[FileSummary]:
        """Process a single file and extract analysis data."""
        try:
            # Check cache first
            if self.cache_manager:
                cached_result = self.cache_manager.get(file_path)
                if cached_result:
                    logger.debug(f"Cache hit for {file_path}")
                    return cached_result
            
            # Detect language
            language = self.language_detector.detect_language(file_path)
            if not language:
                return None
            
            # Get parser
            parser = self.parser_registry.get_parser(language)
            if not parser:
                logger.warning(f"No parser available for {language}")
                return None
            
            # Parse file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            parsed_data = parser.parse(content, str(file_path))
            
            # Create file summary
            summary = FileSummary(
                file_path=str(file_path.relative_to(self.root_path)),
                language=language,
                loc=len([line for line in content.splitlines() if line.strip()]),
                dependencies=parsed_data.get("dependencies", []),
                functions=parsed_data.get("functions", []),
                classes=parsed_data.get("classes", []),
                comments=parsed_data.get("comments", [])
            )
            
            # Cache result
            if self.cache_manager:
                self.cache_manager.put(file_path, summary)
            
            return summary
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return None
    
    def _build_repo_summary(self, file_summaries: Dict[str, FileSummary]) -> RepoSummary:
        """Build repository-level summary from file summaries."""
        all_languages = set()
        all_dependencies = []
        all_functions = []
        all_classes = []
        all_comments = []
        total_files = len(file_summaries)
        total_loc = 0
        per_language_stats = {}
        
        for summary in file_summaries.values():
            all_languages.add(summary.language)
            all_dependencies.extend(summary.dependencies)
            all_functions.extend(summary.functions)
            all_classes.extend(summary.classes)
            all_comments.extend(summary.comments)
            total_loc += summary.loc
            
            # Per-language stats
            if summary.language not in per_language_stats:
                per_language_stats[summary.language] = {"files": 0, "loc": 0}
            per_language_stats[summary.language]["files"] += 1
            per_language_stats[summary.language]["loc"] += summary.loc
        
        # Build scopes for directory and file level
        scopes = self._build_scopes(file_summaries)
        
        return RepoSummary(
            root=str(self.root_path),
            languages=sorted(all_languages),
            summary={
                "total_files": total_files,
                "total_loc": total_loc,
                "per_language": per_language_stats
            },
            dependencies=all_dependencies,
            functions=all_functions,
            classes=all_classes,
            comments=all_comments,
            scopes=scopes,
            generated_at=datetime.now()
        )
    
    def _build_scopes(self, file_summaries: Dict[str, FileSummary]) -> Dict[str, Any]:
        """Build directory and file scopes from file summaries."""
        scopes = {"dir": {}, "file": {}}
        
        # File scopes (direct mapping)
        for file_path, summary in file_summaries.items():
            scopes["file"][file_path] = {
                "dependencies": summary.dependencies,
                "functions": summary.functions,
                "classes": summary.classes,
                "comments": summary.comments
            }
        
        # Directory scopes (aggregated)
        dir_data = {}
        for file_path, summary in file_summaries.items():
            dir_path = str(Path(file_path).parent)
            if dir_path == ".":
                dir_path = "root"
            
            if dir_path not in dir_data:
                dir_data[dir_path] = {
                    "dependencies": [],
                    "functions": [],
                    "classes": [],
                    "comments": []
                }
            
            dir_data[dir_path]["dependencies"].extend(summary.dependencies)
            dir_data[dir_path]["functions"].extend(summary.functions)
            dir_data[dir_path]["classes"].extend(summary.classes)
            dir_data[dir_path]["comments"].extend(summary.comments)
        
        scopes["dir"] = dir_data
        return scopes
    
    def _generate_outputs(self, repo_summary: RepoSummary, file_summaries: Dict[str, FileSummary]):
        """Generate markdown and structured outputs based on configuration."""
        # Generate structured output if requested
        if self.config.get("out") or self.config.get("format") != "md":
            self.structured_formatter.generate(repo_summary, self.config.get("out"))
        
        # Generate markdown outputs if enabled
        if self.config.get("write_md", True):
            if self.config.get("by_file"):
                self._generate_file_markdown(file_summaries)
            elif self.config.get("by_dir"):
                self._generate_directory_markdown(repo_summary)
            else:
                self._generate_repo_markdown(repo_summary)
    
    def _generate_repo_markdown(self, repo_summary: RepoSummary):
        """Generate repository-level markdown."""
        output_path = self._get_output_path("repo", repo_summary.languages[0] if repo_summary.languages else "mixed")
        self.markdown_formatter.generate_repo_markdown(repo_summary, output_path)
        logger.info(f"Generated repository markdown: {output_path}")
    
    def _generate_directory_markdown(self, repo_summary: RepoSummary):
        """Generate per-directory markdown files."""
        output_dir = Path(self.config.get("output_dir", "."))
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for dir_path, dir_data in repo_summary.scopes["dir"].items():
            # Determine primary language for this directory
            languages = set()
            for func in dir_data["functions"]:
                languages.add(func.language)
            for cls in dir_data["classes"]:
                languages.add(cls.language)
            
            primary_lang = list(languages)[0] if languages else "mixed"
            output_path = output_dir / self._get_filename(dir_path, primary_lang)
            
            # Create directory summary
            dir_summary = DirectorySummary(
                directory=dir_path,
                languages=list(languages),
                dependencies=dir_data["dependencies"],
                functions=dir_data["functions"],
                classes=dir_data["classes"],
                comments=dir_data["comments"]
            )
            
            self.markdown_formatter.generate_directory_markdown(dir_summary, output_path)
            logger.info(f"Generated directory markdown: {output_path}")
    
    def _generate_file_markdown(self, file_summaries: Dict[str, FileSummary]):
        """Generate per-file markdown files."""
        output_dir_str = self.config.get("output_dir") or "."
        output_dir = Path(output_dir_str)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for file_path, summary in file_summaries.items():
            file_name = Path(file_path).stem
            output_path = output_dir / self._get_filename(file_name, summary.language)
            self.markdown_formatter.generate_file_markdown(summary, output_path)
            logger.info(f"Generated file markdown: {output_path}")
    
    def _get_output_path(self, name: str, language: str) -> Path:
        """Get output path for a given name and language."""
        if self.config.get("output_dir"):
            base_dir = Path(self.config["output_dir"])
        else:
            base_dir = Path(".")
        
        return base_dir / self._get_filename(name, language)
    
    def _get_filename(self, name: str, language: str) -> str:
        """Generate filename using template."""
        template = self.config.get("md_template", "{{dir}}_code_{{suffix}}.md")
        
        # Get language suffix
        config = LANGUAGE_CONFIGS.get(language)
        suffix = config.suffix if config else "x"
        
        # Simple template replacement
        filename = template.replace("{{dir}}", name.replace("/", "_"))
        filename = filename.replace("{{suffix}}", suffix)
        filename = filename.replace("{{lang}}", language)
        
        return filename