"""Data models for CBIG."""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
from pathlib import Path


class Dependency(BaseModel):
    """Represents a library/package dependency."""
    language: str
    name: str
    version: Optional[str] = None
    source: Optional[str] = None  # pip, npm, cargo, etc.
    group: Optional[str] = None  # for Java groupId
    artifact: Optional[str] = None  # for Java artifactId


class Function(BaseModel):
    """Represents a function or method."""
    language: str
    file: str
    name: str
    signature: str
    line_start: int
    line_end: int
    docstring: Optional[str] = None
    is_method: bool = False
    class_name: Optional[str] = None


class Class(BaseModel):
    """Represents a class, struct, or type."""
    language: str
    file: str
    name: str
    kind: str  # class, struct, interface, enum, etc.
    inherits: Optional[str] = None
    implements: List[str] = Field(default_factory=list)
    line_start: int
    line_end: int
    doc: Optional[str] = None


class Comment(BaseModel):
    """Represents a top-level comment block."""
    language: str
    file: str
    line_start: int
    line_end: int
    text: str


class FileSummary(BaseModel):
    """Summary data for a single file."""
    file_path: str
    language: str
    loc: int  # lines of code
    dependencies: List[Dependency] = Field(default_factory=list)
    functions: List[Function] = Field(default_factory=list)
    classes: List[Class] = Field(default_factory=list)
    comments: List[Comment] = Field(default_factory=list)


class DirectorySummary(BaseModel):
    """Summary data for a directory."""
    directory: str
    languages: List[str] = Field(default_factory=list)
    files: List[str] = Field(default_factory=list)
    total_loc: int = 0
    dependencies: List[Dependency] = Field(default_factory=list)
    functions: List[Function] = Field(default_factory=list)
    classes: List[Class] = Field(default_factory=list)
    comments: List[Comment] = Field(default_factory=list)


class RepoSummary(BaseModel):
    """Complete repository analysis result."""
    root: str
    languages: List[str] = Field(default_factory=list)
    summary: Dict[str, Any] = Field(default_factory=dict)
    dependencies: List[Dependency] = Field(default_factory=list)
    functions: List[Function] = Field(default_factory=list)
    classes: List[Class] = Field(default_factory=list)
    comments: List[Comment] = Field(default_factory=list)
    scopes: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=datetime.now)


class LanguageConfig(BaseModel):
    """Configuration for a specific language parser."""
    name: str
    extensions: List[str]
    suffix: str  # single letter suffix for output files
    tree_sitter_lang: Optional[str] = None
    enabled: bool = True


LANGUAGE_CONFIGS = {
    "python": LanguageConfig(
        name="python",
        extensions=[".py", ".pyi"],
        suffix="p",
        tree_sitter_lang="python"
    ),
    "java": LanguageConfig(
        name="java",
        extensions=[".java"],
        suffix="j",
        tree_sitter_lang="java"
    ),
    "javascript": LanguageConfig(
        name="javascript",
        extensions=[".js", ".jsx", ".mjs", ".cjs"],
        suffix="n",  # n for Node
        tree_sitter_lang="javascript"
    ),
    "typescript": LanguageConfig(
        name="typescript",
        extensions=[".ts", ".tsx"],
        suffix="t",
        tree_sitter_lang="typescript"
    ),
    "html": LanguageConfig(
        name="html",
        extensions=[".html", ".htm"],
        suffix="h",
        tree_sitter_lang="html"
    ),
    "rust": LanguageConfig(
        name="rust",
        extensions=[".rs"],
        suffix="r",
        tree_sitter_lang="rust"
    ),
    "swift": LanguageConfig(
        name="swift",
        extensions=[".swift"],
        suffix="s",
        tree_sitter_lang="swift"
    )
}