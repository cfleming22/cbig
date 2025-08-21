"""Base parser interface for language-specific parsers."""

from abc import ABC, abstractmethod
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class BaseParser(ABC):
    """Abstract base class for language-specific parsers."""
    
    @abstractmethod
    def parse(self, content: str, file_path: str) -> Dict[str, Any]:
        """
        Parse source code content and extract structured information.
        
        Args:
            content: The source code content as a string
            file_path: Path to the file being parsed (for context)
        
        Returns:
            Dictionary containing:
            - dependencies: List of Dependency objects
            - functions: List of Function objects  
            - classes: List of Class objects
            - comments: List of Comment objects
        """
        pass
    
    @abstractmethod
    def get_language(self) -> str:
        """Return the language this parser handles."""
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        """Return parser version for caching purposes."""
        pass
    
    def validate_content(self, content: str) -> bool:
        """
        Validate that content can be parsed.
        
        Default implementation always returns True.
        Subclasses can override for language-specific validation.
        """
        return True
    
    def extract_dependencies(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract import/dependency information."""
        return []
    
    def extract_functions(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract function/method definitions."""
        return []
    
    def extract_classes(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract class/type definitions."""
        return []
    
    def extract_comments(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract top-level comments."""
        return []
    
    def _safe_parse(self, content: str, file_path: str) -> Dict[str, Any]:
        """
        Safely parse content with error handling.
        
        This is a helper method that can be used by subclasses.
        """
        try:
            if not self.validate_content(content):
                logger.warning(f"Content validation failed for {file_path}")
                return self._empty_result()
            
            return {
                'dependencies': self.extract_dependencies(content, file_path),
                'functions': self.extract_functions(content, file_path),
                'classes': self.extract_classes(content, file_path),
                'comments': self.extract_comments(content, file_path)
            }
        
        except Exception as e:
            logger.error(f"Parse error in {file_path}: {e}")
            return self._empty_result()
    
    def _empty_result(self) -> Dict[str, Any]:
        """Return empty parsing result."""
        return {
            'dependencies': [],
            'functions': [],
            'classes': [],
            'comments': []
        }