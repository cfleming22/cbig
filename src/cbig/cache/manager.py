"""Cache manager for storing and retrieving parsed file results."""

import hashlib
import json
import pickle
from pathlib import Path
from typing import Optional, Dict, Any
import logging
import os

from cbig.core.models import FileSummary

logger = logging.getLogger(__name__)


class CacheManager:
    """Manages caching of parsed file results to avoid re-parsing unchanged files."""
    
    def __init__(self, cache_dir: Path):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache metadata
        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()
        
        logger.debug(f"Cache manager initialized with directory: {self.cache_dir}")
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load cache metadata."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load cache metadata: {e}")
        
        return {
            "version": "1.0.0",
            "entries": {}
        }
    
    def _save_metadata(self):
        """Save cache metadata."""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save cache metadata: {e}")
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of file content."""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            return hashlib.sha256(content).hexdigest()
        except Exception as e:
            logger.error(f"Failed to calculate hash for {file_path}: {e}")
            return ""
    
    def _get_cache_key(self, file_path: Path) -> str:
        """Generate cache key for a file."""
        # Use relative path and hash for cache key
        file_hash = self._get_file_hash(file_path)
        return f"{file_hash}"
    
    def _get_cache_file_path(self, cache_key: str) -> Path:
        """Get the cache file path for a given cache key."""
        # Use first 2 chars of hash for subdirectory to avoid too many files in one dir
        subdir = cache_key[:2]
        cache_subdir = self.cache_dir / subdir
        cache_subdir.mkdir(exist_ok=True)
        return cache_subdir / f"{cache_key}.pkl"
    
    def get(self, file_path: Path) -> Optional[FileSummary]:
        """
        Retrieve cached result for a file.
        
        Returns None if no valid cache entry exists.
        """
        try:
            cache_key = self._get_cache_key(file_path)
            if not cache_key:
                return None
            
            # Check if entry exists in metadata
            str_path = str(file_path)
            if str_path not in self.metadata["entries"]:
                return None
            
            entry = self.metadata["entries"][str_path]
            
            # Verify cache key matches (file hasn't changed)
            if entry.get("cache_key") != cache_key:
                logger.debug(f"Cache miss for {file_path}: file changed")
                return None
            
            # Check if cache file exists
            cache_file = self._get_cache_file_path(cache_key)
            if not cache_file.exists():
                logger.debug(f"Cache miss for {file_path}: cache file not found")
                return None
            
            # Load cached result
            with open(cache_file, 'rb') as f:
                result = pickle.load(f)
            
            logger.debug(f"Cache hit for {file_path}")
            return result
            
        except Exception as e:
            logger.warning(f"Cache retrieval failed for {file_path}: {e}")
            return None
    
    def put(self, file_path: Path, result: FileSummary):
        """Store result in cache."""
        try:
            cache_key = self._get_cache_key(file_path)
            if not cache_key:
                return
            
            # Save result to cache file
            cache_file = self._get_cache_file_path(cache_key)
            with open(cache_file, 'wb') as f:
                pickle.dump(result, f)
            
            # Update metadata
            str_path = str(file_path)
            self.metadata["entries"][str_path] = {
                "cache_key": cache_key,
                "file_size": file_path.stat().st_size,
                "modified_time": file_path.stat().st_mtime,
                "cached_at": os.path.getmtime(cache_file)
            }
            
            self._save_metadata()
            logger.debug(f"Cached result for {file_path}")
            
        except Exception as e:
            logger.error(f"Cache storage failed for {file_path}: {e}")
    
    def clear(self):
        """Clear all cache entries."""
        try:
            # Remove all cache files
            for cache_file in self.cache_dir.rglob("*.pkl"):
                cache_file.unlink()
            
            # Reset metadata
            self.metadata = {
                "version": "1.0.0",
                "entries": {}
            }
            self._save_metadata()
            
            logger.info("Cache cleared")
            
        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        try:
            total_entries = len(self.metadata["entries"])
            
            # Count actual cache files
            cache_files = list(self.cache_dir.rglob("*.pkl"))
            total_files = len(cache_files)
            
            # Calculate total size
            total_size = sum(f.stat().st_size for f in cache_files)
            
            return {
                "total_entries": total_entries,
                "total_files": total_files,
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "cache_dir": str(self.cache_dir)
            }
            
        except Exception as e:
            logger.error(f"Failed to get cache stats: {e}")
            return {}
    
    def cleanup_orphaned(self):
        """Remove orphaned cache files that are no longer referenced."""
        try:
            # Get all referenced cache keys
            referenced_keys = set()
            for entry in self.metadata["entries"].values():
                referenced_keys.add(entry.get("cache_key"))
            
            # Find orphaned cache files
            orphaned = []
            for cache_file in self.cache_dir.rglob("*.pkl"):
                cache_key = cache_file.stem
                if cache_key not in referenced_keys:
                    orphaned.append(cache_file)
            
            # Remove orphaned files
            for cache_file in orphaned:
                cache_file.unlink()
                logger.debug(f"Removed orphaned cache file: {cache_file}")
            
            if orphaned:
                logger.info(f"Cleaned up {len(orphaned)} orphaned cache files")
            
        except Exception as e:
            logger.error(f"Cache cleanup failed: {e}")