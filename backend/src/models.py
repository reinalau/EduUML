"""Data models for the UML generator."""

from typing import Dict, Any, Optional
from pydantic import BaseModel
from enum import Enum


class DiagramType(str, Enum):
    """Supported UML diagram types."""
    CLASS = "class"
    SEQUENCE = "sequence"
    COMPONENT = "component"
    OBJECT = "object"
    DEPLOYMENT = "deployment"
    USE_CASE = "use_case"
    ACTIVITY = "activity"
    STATE = "state"


class OutputFormat(str, Enum):
    """Supported output formats."""
    DRAWIO = "drawio"
    PLANTUML = "plantuml"
    MERMAID = "mermaid"


class AnalysisMethod(str, Enum):
    """Analysis methods available."""
    LLM_DIRECT = "llm_direct"    # Direct LLM analysis


class AnalysisRequest(BaseModel):
    """Request model for code analysis."""
    repo_url: Optional[str] = None
    local_directory: Optional[str] = None
    code_files: Optional[Dict[str, str]] = None
    diagram_type: DiagramType
    output_format: OutputFormat
    analysis_method: AnalysisMethod = AnalysisMethod.LLM_DIRECT
    filters: Optional[Dict[str, Any]] = None


class DiagramResponse(BaseModel):
    """Response model for generated diagram."""
    diagram_code: str
    format: OutputFormat
    metadata: Dict[str, Any]
    success: bool
    error: Optional[str] = None