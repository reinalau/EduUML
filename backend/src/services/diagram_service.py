"""Main service for generating UML diagrams from code repositories."""

import logging
import os
from typing import Dict, List, Optional
from ..models import AnalysisRequest, DiagramResponse, AnalysisMethod
from ..llm.gemini_provider import GeminiProvider
from .github_service import GitHubService
from .local_directory_service import LocalDirectoryService

logger = logging.getLogger(__name__)


class DiagramService:
    """Main service for processing diagram generation requests."""
    
    def __init__(self):
        self.github_service = GitHubService()
        self.local_directory_service = LocalDirectoryService()
        
        # Initialize Gemini provider
        try:
            self.llm_provider = GeminiProvider()
            logger.info("Gemini provider initialized successfully")
        except Exception as e:
            logger.error(f"Could not initialize Gemini provider: {str(e)}")
            self.llm_provider = None
    
    def generate_diagram(self, request: AnalysisRequest) -> DiagramResponse:
        """
        Generate UML diagram from various sources.
        
        Args:
            request: Analysis request with source and parameters
            
        Returns:
            Diagram response with generated code
        """
        try:
            # Determine source type and get source files
            if request.repo_url:
                return self._generate_from_github_repo(request)
            elif request.local_directory:
                return self._generate_from_local_directory(request)
            elif request.code_files:
                return self._generate_from_code_files(request)
            else:
                return DiagramResponse(
                    diagram_code="",
                    format=request.output_format,
                    metadata={"error": "No source specified (repo_url, local_directory, or code_files)"},
                    success=False,
                    error="No source specified"
                )
                
        except Exception as e:
            logger.error(f"Error generating diagram: {str(e)}")
            return DiagramResponse(
                diagram_code="",
                format=request.output_format,
                metadata={"error": str(e)},
                success=False,
                error=str(e)
            )
    
    def _generate_from_local_directory(self, request: AnalysisRequest) -> DiagramResponse:
        """Generate diagram from local directory."""
        try:
            logger.info(f"Processing local directory: {request.local_directory}")
            
            # Get source files from local directory
            source_files = self.local_directory_service.get_source_files(request.local_directory)
            directory_info = self.local_directory_service.get_directory_info(request.local_directory)
            
            if not source_files:
                return DiagramResponse(
                    diagram_code="",
                    format=request.output_format,
                    metadata={"error": "No supported source files found in directory"},
                    success=False,
                    error="No supported source files found"
                )
            
            # Generate diagram using LLM
            return self._generate_with_direct_llm(request, source_files, directory_info)
                
        except Exception as e:
            logger.error(f"Error processing local directory: {str(e)}")
            return DiagramResponse(
                diagram_code="",
                format=request.output_format,
                metadata={"error": str(e)},
                success=False,
                error=str(e)
            )
    
    def _generate_from_code_files(self, request: AnalysisRequest) -> DiagramResponse:
        """Generate diagram from provided code files."""
        try:
            logger.info(f"Processing {len(request.code_files)} provided code files")
            
            # Generate diagram using LLM
            return self._generate_with_direct_llm(request, request.code_files, {"type": "code_files"})
                
        except Exception as e:
            logger.error(f"Error processing code files: {str(e)}")
            return DiagramResponse(
                diagram_code="",
                format=request.output_format,
                metadata={"error": str(e)},
                success=False,
                error=str(e)
            )
    
    def _generate_with_direct_llm(self, request: AnalysisRequest, source_files: Dict[str, str], source_info: Dict) -> DiagramResponse:
        """Generate diagram using direct LLM analysis."""
        if not self.llm_provider:
            return DiagramResponse(
                diagram_code="",
                format=request.output_format,
                metadata={"error": "LLM provider not available for direct analysis"},
                success=False,
                error="LLM provider not available"
            )
        
        try:
            # Check if provider supports direct analysis
            if not hasattr(self.llm_provider, 'generate_diagram_from_source_files'):
                return DiagramResponse(
                    diagram_code="",
                    format=request.output_format,
                    metadata={"error": "LLM provider does not support direct analysis"},
                    success=False,
                    error="Direct analysis not supported by LLM provider"
                )
            
            # Generate diagram directly from source files
            diagram_code, llm_metadata = self.llm_provider.generate_diagram_from_source_files(
                source_files,
                request.diagram_type,
                request.output_format
            )
            
            # Create response metadata
            metadata = {
                "source": source_info,
                "files_analyzed": len(source_files),
                "analysis_method": "llm_direct",
                "llm_provider": type(self.llm_provider).__name__,
                "llm_metadata": llm_metadata
            }
            
            return DiagramResponse(
                diagram_code=diagram_code,
                format=request.output_format,
                metadata=metadata,
                success=True
            )
            
        except Exception as e:
            logger.error(f"Error in direct LLM analysis: {str(e)}")
            return DiagramResponse(
                diagram_code="",
                format=request.output_format,
                metadata={"error": str(e)},
                success=False,
                error=str(e)
            )
    
    def _generate_from_github_repo(self, request: AnalysisRequest) -> DiagramResponse:
        """Generate UML diagram from GitHub repository URL."""
        try:
            logger.info(f"Processing request for repo: {request.repo_url}")
            
            if not self.llm_provider:
                return DiagramResponse(
                    diagram_code="",
                    format=request.output_format,
                    metadata={"error": "LLM provider not available"},
                    success=False,
                    error="LLM provider not available"
                )
            
            # Generate diagram directly from GitHub URL
            diagram_code, llm_metadata = self.llm_provider.generate_diagram_from_github_url(
                request.repo_url,
                request.diagram_type,
                request.output_format
            )
            
            # Create response metadata
            metadata = {
                "source": {"repository_url": request.repo_url},
                "analysis_method": "llm_direct",
                "llm_provider": type(self.llm_provider).__name__,
                "llm_metadata": llm_metadata
            }
            
            return DiagramResponse(
                diagram_code=diagram_code,
                format=request.output_format,
                metadata=metadata,
                success=True
            )
            
        except Exception as e:
            logger.error(f"Error generating diagram from GitHub: {str(e)}")
            return DiagramResponse(
                diagram_code="",
                format=request.output_format,
                metadata={"error": str(e)},
                success=False,
                error=str(e)
            )
