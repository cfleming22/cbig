"""Parser registry for managing language-specific parsers."""

from typing import Dict, Optional, Any
import logging

from cbig.parsers.base import BaseParser
from cbig.parsers.python_parser import PythonParser
from cbig.parsers.java_parser import JavaParser
from cbig.parsers.javascript_parser import JavaScriptParser
from cbig.parsers.html_parser import HTMLParser
from cbig.parsers.rust_parser import RustParser
from cbig.parsers.generic_parser import GenericParser

logger = logging.getLogger(__name__)


class ParserRegistry:
    """Registry for managing language-specific parsers."""
    
    def __init__(self):
        self._parsers: Dict[str, BaseParser] = {}
        self._initialize_parsers()
    
    def _initialize_parsers(self):
        """Initialize all available parsers."""
        parser_classes = {
            'python': PythonParser,
            'java': JavaParser,
            'javascript': JavaScriptParser,
            'typescript': JavaScriptParser,  # TypeScript uses JS parser
            'jsx': JavaScriptParser,
            'html': HTMLParser,
            'rust': RustParser,
            'swift': GenericParser,  # Swift will use generic parser for now
        }
        
        for language, parser_class in parser_classes.items():
            try:
                self._parsers[language] = parser_class()
                logger.debug(f"Initialized parser for {language}")
            except Exception as e:
                logger.warning(f"Failed to initialize parser for {language}: {e}")
                # Fall back to generic parser
                self._parsers[language] = GenericParser()
    
    def get_parser(self, language: str) -> Optional[BaseParser]:
        """Get parser for a specific language."""
        parser = self._parsers.get(language)
        if not parser:
            # Fall back to generic parser
            logger.debug(f"No specific parser for {language}, using generic parser")
            return GenericParser()
        return parser
    
    def list_supported_languages(self) -> list:
        """List all supported languages."""
        return list(self._parsers.keys())
    
    def register_parser(self, language: str, parser: BaseParser):
        """Register a custom parser for a language."""
        self._parsers[language] = parser
        logger.info(f"Registered custom parser for {language}")