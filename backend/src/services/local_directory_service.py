"""Local directory service for analyzing local code repositories."""

import os
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


# Supported file extensions for source code
SUPPORTED_EXTENSIONS = [
    '.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', 
    '.php', '.rb', '.go', '.kt', '.swift', '.rs', '.scala', 
    '.yaml', '.yml', '.tf', '.tfvars'
]


class LocalDirectoryService:
    """Service for handling local directory operations."""
    
    def __init__(self):
        pass
    
    def get_source_files(self, directory_path: str, max_files: int = 100) -> Dict[str, str]:
        """
        Get source code files from local directory.
        
        Args:
            directory_path: Path to local directory
            max_files: Maximum number of files to process
            
        Returns:
            Dictionary mapping file paths to file contents
        """
        if not os.path.exists(directory_path):
            raise ValueError(f"Directory does not exist: {directory_path}")
        
        if not os.path.isdir(directory_path):
            raise ValueError(f"Path is not a directory: {directory_path}")
        
        source_files = {}
        file_count = 0
        
        logger.info(f"Scanning directory: {directory_path}")
        logger.info(f"Supported extensions: {SUPPORTED_EXTENSIONS}")
        
        try:
            for root, dirs, files in os.walk(directory_path):
                # Log directory being processed
                logger.info(f"Processing directory: {root}")
                
                # Skip common non-source directories
                original_dirs = dirs.copy()
                dirs[:] = [d for d in dirs if not self._should_skip_directory(d)]
                
                if len(dirs) != len(original_dirs):
                    skipped = set(original_dirs) - set(dirs)
                    logger.info(f"Skipped directories: {skipped}")
                
                logger.info(f"Will process subdirectories: {dirs}")
                
                for file in files:
                    if file_count >= max_files:
                        logger.warning(f"Reached maximum file limit ({max_files})")
                        break
                    
                    # Log each file being checked
                    logger.debug(f"Checking file: {file}")
                    
                    # Check if file has supported extension
                    if any(file.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, directory_path)
                        
                        logger.info(f"Found supported file: {relative_path}")
                        
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                
                                # Skip very large files (>100KB)
                                if len(content) > 100000:
                                    logger.warning(f"Skipping large file: {relative_path}")
                                    continue
                                
                                source_files[relative_path] = content
                                file_count += 1
                                logger.info(f"Added file {file_count}: {relative_path}")
                                
                        except Exception as e:
                            logger.warning(f"Could not read file {relative_path}: {str(e)}")
                            continue
                    else:
                        logger.debug(f"Skipped unsupported file: {file}")
                
                if file_count >= max_files:
                    break
            
            logger.info(f"Found {len(source_files)} source files in {directory_path}")
            logger.info(f"Files found: {list(source_files.keys())}")
            return source_files
            
        except Exception as e:
            logger.error(f"Error reading source files: {str(e)}")
            return {}
    
    def get_directory_info(self, directory_path: str) -> Dict[str, str]:
        """
        Extract directory information.
        
        Args:
            directory_path: Path to local directory
            
        Returns:
            Dictionary with directory info
        """
        try:
            abs_path = os.path.abspath(directory_path)
            dir_name = os.path.basename(abs_path)
            
            return {
                'name': dir_name,
                'path': abs_path,
                'type': 'local_directory'
            }
            
        except Exception as e:
            logger.warning(f"Could not parse directory info: {str(e)}")
            return {'path': directory_path, 'type': 'local_directory'}
    
    def _should_skip_directory(self, dirname: str) -> bool:
        """Check if directory should be skipped during file scanning."""
        skip_dirs = {
            '.git', '.svn', '.hg',  # Version control
            'node_modules', 'venv', 'env', '__pycache__',  # Dependencies/cache
            '.pytest_cache', '.mypy_cache', '.tox',  # Testing/linting cache
            'build', 'dist', 'target', 'out',  # Build outputs
            '.idea', '.vscode', '.vs',  # IDE files
            'logs', 'tmp', 'temp'  # Temporary files
        }
        return dirname.lower() in skip_dirs or dirname.startswith('.')