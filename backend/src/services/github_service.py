"""GitHub repository service for downloading and analyzing repositories."""

import os
import tempfile
import shutil
import logging
import requests
import zipfile
from typing import Dict, Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


# Supported file extensions for source code
SUPPORTED_EXTENSIONS = [
    '.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', 
    '.php', '.rb', '.go', '.kt', '.swift', '.rs', '.scala',
    '.yaml', '.yml', '.tf', '.tfvars'
]


class GitHubService:
    """Service for handling GitHub repository operations."""
    
    def __init__(self):
        self.temp_dir = None
    
    def clone_repository(self, repo_url: str) -> str:
        """Download GitHub repository as ZIP."""
        if not self._is_valid_github_url(repo_url):
            raise ValueError(f"Invalid GitHub URL: {repo_url}")
        
        self.temp_dir = tempfile.mkdtemp(prefix="uml_repo_")
        
        try:
            zip_url = self._get_zip_download_url(repo_url)
            logger.info(f"Downloading: {zip_url}")
            
            response = requests.get(zip_url, timeout=300)
            response.raise_for_status()
            
            zip_path = os.path.join(self.temp_dir, "repo.zip")
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)
            
            os.remove(zip_path)
            
            extracted_dirs = [d for d in os.listdir(self.temp_dir) 
                            if os.path.isdir(os.path.join(self.temp_dir, d))]
            
            if not extracted_dirs:
                raise RuntimeError("No directory found in ZIP")
            
            repo_path = os.path.join(self.temp_dir, extracted_dirs[0])
            return repo_path
            
        except Exception as e:
            self.cleanup()
            raise RuntimeError(f"Failed to download: {str(e)}")
    
    def get_source_files(self, repo_path: str, max_files: int = 100) -> Dict[str, str]:
        """Get source code files from repository."""
        source_files = {}
        file_count = 0
        
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if not self._should_skip_directory(d)]
            
            for file in files:
                if file_count >= max_files:
                    break
                
                if any(file.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, repo_path)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if len(content) <= 100000:
                                source_files[relative_path] = content
                                file_count += 1
                    except Exception as e:
                        logger.warning(f"Could not read {relative_path}: {str(e)}")
            
            if file_count >= max_files:
                break
        
        return source_files
    
    def get_repository_info(self, repo_url: str) -> Dict[str, str]:
        """Extract repository information from URL."""
        try:
            parsed = urlparse(repo_url)
            path_parts = parsed.path.strip('/').split('/')
            
            if len(path_parts) >= 2:
                owner = path_parts[0]
                repo_name = path_parts[1].replace('.git', '')
                return {
                    'owner': owner,
                    'name': repo_name,
                    'full_name': f"{owner}/{repo_name}",
                    'url': repo_url
                }
            return {'url': repo_url}
        except Exception:
            return {'url': repo_url}
    
    def cleanup(self):
        """Clean up temporary directory."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                logger.info(f"Cleaned up: {self.temp_dir}")
            except Exception as e:
                logger.warning(f"Cleanup failed: {str(e)}")
            finally:
                self.temp_dir = None
    
    def _is_valid_github_url(self, url: str) -> bool:
        """Check if URL is a valid GitHub repository URL."""
        try:
            parsed = urlparse(url)
            return (
                parsed.scheme in ['http', 'https'] and
                parsed.netloc in ['github.com', 'www.github.com'] and
                len(parsed.path.strip('/').split('/')) >= 2
            )
        except Exception:
            return False
    
    def _get_zip_download_url(self, repo_url: str) -> str:
        """Convert GitHub repo URL to ZIP download URL with branch detection."""
        parsed = urlparse(repo_url)
        path_parts = parsed.path.strip('/').split('/')
        
        if len(path_parts) >= 2:
            owner = path_parts[0]
            repo_name = path_parts[1].replace('.git', '')
            
            # Try main branch first, then master as fallback
            for branch in ['main', 'master']:
                zip_url = f"https://github.com/{owner}/{repo_name}/archive/refs/heads/{branch}.zip"
                try:
                    response = requests.head(zip_url, timeout=10)
                    if response.status_code == 200:
                        return zip_url
                except:
                    continue
            
            # Default to main if both fail
            return f"https://github.com/{owner}/{repo_name}/archive/refs/heads/main.zip"
        
        raise ValueError("Invalid GitHub URL format")
    
    def _should_skip_directory(self, dirname: str) -> bool:
        """Check if directory should be skipped."""
        skip_dirs = {
            '.git', '.svn', 'node_modules', '__pycache__', 
            '.pytest_cache', 'build', 'dist', '.idea', '.vscode'
        }
        return dirname.lower() in skip_dirs or dirname.startswith('.')
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()