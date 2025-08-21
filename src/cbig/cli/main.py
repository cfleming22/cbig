"""Main CLI application for CBIG."""

import typer
from typing import Optional, List
from pathlib import Path
import sys
import os
from rich.console import Console
from rich.logging import RichHandler
import logging

from cbig.core.processor import CBIGProcessor
from cbig.core.models import LANGUAGE_CONFIGS

app = typer.Typer(
    name="cbig",
    help="CodeBase Insight Generator - Cross-language CLI extractor for directory-level code analysis",
    rich_markup_mode="rich"
)

console = Console()


def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
    """Setup logging configuration."""
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[RichHandler(console=console, rich_tracebacks=True)]
    )


@app.command()
def main(
    path: str = typer.Option(
        ".",
        "--path", "-p",
        help="Root path (local directory, git URL, or archive)"
    ),
    language: Optional[str] = typer.Option(
        None,
        "--language", "-l",
        help="CSV of languages to include (python,java,rust)"
    ),
    include: List[str] = typer.Option(
        [],
        "--include",
        help="Additional glob patterns to include"
    ),
    exclude: List[str] = typer.Option(
        [],
        "--exclude", 
        help="Glob patterns to exclude"
    ),
    by_dir: bool = typer.Option(
        False,
        "--by-dir",
        help="Emit one markdown per directory"
    ),
    by_file: bool = typer.Option(
        False,
        "--by-file",
        help="Emit one markdown per file"
    ),
    md_template: str = typer.Option(
        "{{dir}}_code_{{suffix}}.md",
        "--md-template",
        help="Jinja-style filename template"
    ),
    write_md: bool = typer.Option(
        True,
        "--write-md/--no-md",
        help="Force/suppress markdown generation"
    ),
    output_dir: Optional[str] = typer.Option(
        None,
        "--output-dir",
        help="Directory where markdown files are written"
    ),
    format: str = typer.Option(
        "json",
        "--format", "-f",
        help="Output format for structured report (json, yaml, md, txt)"
    ),
    out: Optional[str] = typer.Option(
        None,
        "--out", "-o",
        help="File path for structured report"
    ),
    summary: bool = typer.Option(
        True,
        "--summary/--no-summary",
        help="Include summary section"
    ),
    deps: bool = typer.Option(
        True,
        "--deps/--no-deps",
        help="Include dependencies section"
    ),
    functions: bool = typer.Option(
        True,
        "--functions/--no-functions",
        help="Include functions section"
    ),
    classes: bool = typer.Option(
        True,
        "--classes/--no-classes",
        help="Include classes section"
    ),
    comments: bool = typer.Option(
        False,
        "--comments/--no-comments",
        help="Include comments section"
    ),
    sort: List[str] = typer.Option(
        [],
        "--sort",
        help="Sorting rule per section (functions=name)"
    ),
    max_workers: int = typer.Option(
        None,
        "--max-workers", "-j",
        help="Parallel workers (default = CPU count)"
    ),
    cache_dir: Optional[str] = typer.Option(
        None,
        "--cache-dir",
        help="Where to store AST cache"
    ),
    clear_cache: bool = typer.Option(
        False,
        "--clear-cache",
        help="Clear cache before processing"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Verbose logging"
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet", "-q",
        help="Quiet mode (errors only)"
    )
):
    """
    Generate directory-level code insights with libraries, functions, and classes.
    
    Examples:
        cbig -p ./myrepo                           # Repo-wide analysis
        cbig -p . --by-dir --output-dir docs/     # Per-directory markdown
        cbig -p src/user.py --by-file              # Single file analysis
        cbig -p . --format yaml -o report.yaml    # Structured output only
    """
    setup_logging(verbose, quiet)
    logger = logging.getLogger(__name__)
    
    try:
        # Parse language filter
        languages = None
        if language:
            languages = [lang.strip() for lang in language.split(",")]
            # Validate languages
            invalid_langs = set(languages) - set(LANGUAGE_CONFIGS.keys())
            if invalid_langs:
                console.print(f"[red]Error: Unknown languages: {', '.join(invalid_langs)}[/red]")
                console.print(f"Available languages: {', '.join(LANGUAGE_CONFIGS.keys())}")
                raise typer.Exit(4)
        
        # Parse sort options
        sort_options = {}
        for sort_rule in sort:
            if "=" not in sort_rule:
                console.print(f"[red]Error: Invalid sort format '{sort_rule}'. Use format: section=field[/red]")
                raise typer.Exit(1)
            section, field = sort_rule.split("=", 1)
            sort_options[section] = field
        
        # Set max_workers to CPU count if not specified
        if max_workers is None:
            max_workers = os.cpu_count()
        
        # Auto-enable by_dir if output_dir is specified
        if output_dir and not by_file:
            by_dir = True
        
        # Create processor configuration
        config = {
            "path": path,
            "languages": languages,
            "include": include,
            "exclude": exclude,
            "by_dir": by_dir,
            "by_file": by_file,
            "md_template": md_template,
            "write_md": write_md,
            "output_dir": output_dir,
            "format": format,
            "out": out,
            "sections": {
                "summary": summary,
                "deps": deps,
                "functions": functions,
                "classes": classes,
                "comments": comments
            },
            "sort_options": sort_options,
            "max_workers": max_workers,
            "cache_dir": cache_dir,
            "clear_cache": clear_cache
        }
        
        # Create and run processor
        processor = CBIGProcessor(config)
        result = processor.process()
        
        if not quiet:
            console.print(f"[green]✅ Analysis complete![/green]")
            console.print(f"Processed {len(result.summary.get('per_language', {}))} languages")
            console.print(f"Total files: {result.summary.get('total_files', 0)}")
            console.print(f"Total LOC: {result.summary.get('total_loc', 0)}")
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        console.print("[yellow]⚠️  Operation cancelled by user[/yellow]")
        sys.exit(1)
    except FileNotFoundError as e:
        console.print(f"[red]Error: File not found: {e}[/red]")
        sys.exit(3)
    except PermissionError as e:
        console.print(f"[red]Error: Permission denied: {e}[/red]")
        sys.exit(3)
    except Exception as e:
        logger.exception("Unexpected error occurred")
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(2)


@app.command()
def version():
    """Show version information."""
    from cbig import __version__
    console.print(f"CBIG version {__version__}")


@app.command()
def languages():
    """List supported languages and their configurations."""
    console.print("[bold]Supported Languages:[/bold]\n")
    
    for lang_name, config in LANGUAGE_CONFIGS.items():
        console.print(f"[cyan]{lang_name}[/cyan] (suffix: {config.suffix})")
        console.print(f"  Extensions: {', '.join(config.extensions)}")
        console.print(f"  Tree-sitter: {config.tree_sitter_lang or 'N/A'}")
        console.print(f"  Enabled: {'✅' if config.enabled else '❌'}")
        console.print()


if __name__ == "__main__":
    app()