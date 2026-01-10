"""Unit tests for GitHub service."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.github_service import GitHubService


class TestGitHubService:
    """Test cases for GitHubService."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.service = GitHubService()
    
    def test_is_valid_github_url(self):
        """Test GitHub URL validation."""
        valid_urls = [
            "https://github.com/user/repo",
            "https://github.com/user/repo.git",
            "http://github.com/user/repo",
            "https://www.github.com/user/repo"
        ]
        
        invalid_urls = [
            "https://gitlab.com/user/repo",
            "https://github.com/user",
            "https://github.com",
            "not-a-url",
            ""
        ]
        
        for url in valid_urls:
            assert self.service._is_valid_github_url(url), f"Should be valid: {url}"
        
        for url in invalid_urls:
            assert not self.service._is_valid_github_url(url), f"Should be invalid: {url}"
    
    def test_should_skip_directory(self):
        """Test directory skipping logic."""
        skip_dirs = [
            ".git", "node_modules", "__pycache__", ".pytest_cache",
            "build", "dist", ".idea", ".vscode", ".svn"
        ]
        
        keep_dirs = [
            "src", "lib", "components", "utils", "tests", "docs", "logs"
        ]
        
        for dirname in skip_dirs:
            assert self.service._should_skip_directory(dirname), f"Should skip: {dirname}"
        
        for dirname in keep_dirs:
            assert not self.service._should_skip_directory(dirname), f"Should keep: {dirname}"
    
    def test_get_repository_info(self):
        """Test repository info extraction."""
        test_cases = [
            {
                "url": "https://github.com/user/repo",
                "expected": {
                    "owner": "user",
                    "name": "repo",
                    "full_name": "user/repo",
                    "url": "https://github.com/user/repo"
                }
            },
            {
                "url": "https://github.com/user/repo.git",
                "expected": {
                    "owner": "user",
                    "name": "repo",
                    "full_name": "user/repo",
                    "url": "https://github.com/user/repo.git"
                }
            }
        ]
        
        for case in test_cases:
            result = self.service.get_repository_info(case["url"])
            for key, expected_value in case["expected"].items():
                assert result[key] == expected_value
    
    def test_clone_repository_invalid_url(self):
        """Test cloning with invalid URL."""
        invalid_url = "https://invalid-site.com/user/repo"
        
        with pytest.raises(ValueError, match="Invalid GitHub URL"):
            self.service.clone_repository(invalid_url)
    
    def test_get_source_files_returns_dict(self):
        """Test source file extraction returns a dictionary."""
        with patch('os.walk') as mock_walk:
            # Mock minimal directory structure
            mock_walk.return_value = [
                ("/repo", ["src"], ["README.md"]),
                ("/repo/src", [], ["main.py"])
            ]
            
            with patch('builtins.open', create=True) as mock_open_func:
                mock_file = MagicMock()
                mock_file.read.return_value = "def main():\n    pass"
                mock_file.__enter__.return_value = mock_file
                mock_open_func.return_value = mock_file
                
                result = self.service.get_source_files("/repo", max_files=10)
                
                # Result should be a dictionary
                assert isinstance(result, dict)
    
    def test_context_manager(self):
        """Test context manager functionality."""
        service = GitHubService()
        with patch.object(service, 'cleanup') as mock_cleanup:
            with service:
                assert service is not None
            
            # Cleanup should be called on exit
            mock_cleanup.assert_called_once()
