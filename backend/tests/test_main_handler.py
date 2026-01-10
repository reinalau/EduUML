"""Unit tests for main Lambda handler."""

import pytest
import json
from unittest.mock import Mock, patch
from src.handlers.main_handler import lambda_handler, create_success_response, create_error_response
from src.models import DiagramResponse, OutputFormat


class TestMainHandler:
    """Test cases for main Lambda handler."""
    
    def test_create_success_response(self):
        """Test success response creation."""
        data = {"diagram_code": "@startuml\nclass User\n@enduml", "success": True}
        response = create_success_response(data)
        
        assert response['statusCode'] == 200
        assert 'Access-Control-Allow-Origin' in response['headers']
        assert response['headers']['Content-Type'] == 'application/json'
        
        body = json.loads(response['body'])
        assert body['diagram_code'] == "@startuml\nclass User\n@enduml"
        assert body['success'] is True
    
    def test_create_error_response(self):
        """Test error response creation."""
        response = create_error_response(400, "Invalid request")
        
        assert response['statusCode'] == 400
        assert 'Access-Control-Allow-Origin' in response['headers']
        
        body = json.loads(response['body'])
        assert body['error'] == "Invalid request"
        assert body['success'] is False
    
    def test_missing_source_and_required_fields(self):
        """Test handling of missing source and required fields."""
        event = {
            'body': json.dumps({
                # Missing repo_url, local_directory, and code_files
                'diagram_type': 'class'
                # Missing output_format
            })
        }
        
        response = lambda_handler(event, {})
        
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert 'At least one source must be provided' in body['error']
    
    def test_missing_diagram_type(self):
        """Test handling of missing diagram_type."""
        event = {
            'body': json.dumps({
                'repo_url': 'https://github.com/user/repo',
                'output_format': 'mermaid'
                # Missing diagram_type
            })
        }
        
        response = lambda_handler(event, {})
        
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert 'Missing required fields' in body['error']
        assert 'diagram_type' in body['error']
    
    def test_missing_output_format(self):
        """Test handling of missing output_format."""
        event = {
            'body': json.dumps({
                'repo_url': 'https://github.com/user/repo',
                'diagram_type': 'class'
                # Missing output_format
            })
        }
        
        response = lambda_handler(event, {})
        
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert 'Missing required fields' in body['error']
        assert 'output_format' in body['error']
    
    def test_invalid_diagram_type(self):
        """Test handling of invalid diagram type."""
        event = {
            'body': json.dumps({
                'repo_url': 'https://github.com/user/repo',
                'diagram_type': 'invalid_type',
                'output_format': 'mermaid'
            })
        }
        
        response = lambda_handler(event, {})
        
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert 'Invalid request parameters' in body['error']
    
    def test_invalid_output_format(self):
        """Test handling of invalid output format."""
        event = {
            'body': json.dumps({
                'repo_url': 'https://github.com/user/repo',
                'diagram_type': 'class',
                'output_format': 'invalid_format'
            })
        }
        
        response = lambda_handler(event, {})
        
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert 'Invalid request parameters' in body['error']
    
    @patch('src.handlers.main_handler.DiagramService')
    def test_successful_request_with_github_url(self, mock_service_class):
        """Test successful diagram generation request with GitHub URL."""
        # Mock service response
        mock_service = Mock()
        mock_response = DiagramResponse(
            diagram_code="graph TD;\n    A[User]\n    B[Account]",
            format=OutputFormat.MERMAID,
            metadata={"repository_url": "https://github.com/user/repo", "analysis_method": "github_url"},
            success=True
        )
        mock_service.generate_diagram.return_value = mock_response
        mock_service_class.return_value = mock_service
        
        # Create valid request with GitHub URL
        event = {
            'body': json.dumps({
                'repo_url': 'https://github.com/user/repo',
                'diagram_type': 'class',
                'output_format': 'mermaid',
                'analysis_method': 'llm_direct'
            })
        }
        
        response = lambda_handler(event, {})
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['diagram_code'] == "graph TD;\n    A[User]\n    B[Account]"
        assert body['format'] == 'mermaid'
        assert body['success'] is True
    
    @patch('src.handlers.main_handler.DiagramService')
    def test_successful_request_with_local_directory(self, mock_service_class):
        """Test successful diagram generation request with local directory."""
        # Mock service response
        mock_service = Mock()
        mock_response = DiagramResponse(
            diagram_code="@startuml\nclass User\n@enduml",
            format=OutputFormat.PLANTUML,
            metadata={"files_analyzed": 5, "analysis_method": "local_directory"},
            success=True
        )
        mock_service.generate_diagram.return_value = mock_response
        mock_service_class.return_value = mock_service
        
        # Create valid request with local directory
        event = {
            'body': json.dumps({
                'local_directory': '/path/to/local/repo',
                'diagram_type': 'class',
                'output_format': 'plantuml'
            })
        }
        
        response = lambda_handler(event, {})
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['diagram_code'] == "@startuml\nclass User\n@enduml"
        assert body['format'] == 'plantuml'
        assert body['success'] is True
        assert body['metadata']['files_analyzed'] == 5
    
    @patch('src.handlers.main_handler.DiagramService')
    def test_successful_request_with_code_files(self, mock_service_class):
        """Test successful diagram generation request with code files."""
        # Mock service response
        mock_service = Mock()
        mock_response = DiagramResponse(
            diagram_code="classDiagram\n    class User\n    class Account",
            format=OutputFormat.MERMAID,
            metadata={"files_analyzed": 2, "analysis_method": "source_files"},
            success=True
        )
        mock_service.generate_diagram.return_value = mock_response
        mock_service_class.return_value = mock_service
        
        # Create valid request with code files
        event = {
            'body': json.dumps({
                'code_files': {
                    'user.py': 'class User:\n    pass',
                    'account.py': 'class Account:\n    pass'
                },
                'diagram_type': 'class',
                'output_format': 'mermaid'
            })
        }
        
        response = lambda_handler(event, {})
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['diagram_code'] == "classDiagram\n    class User\n    class Account"
        assert body['format'] == 'mermaid'
        assert body['success'] is True
    
    @patch('src.handlers.main_handler.DiagramService')
    def test_service_error(self, mock_service_class):
        """Test handling of service errors."""
        # Mock service to raise exception
        mock_service = Mock()
        mock_service.generate_diagram.side_effect = Exception("Service error")
        mock_service_class.return_value = mock_service
        
        event = {
            'body': json.dumps({
                'repo_url': 'https://github.com/user/repo',
                'diagram_type': 'class',
                'output_format': 'mermaid'
            })
        }
        
        response = lambda_handler(event, {})
        
        assert response['statusCode'] == 500
        body = json.loads(response['body'])
        assert 'Internal server error' in body['error']
        assert body['success'] is False
    
    def test_direct_event_body(self):
        """Test handling of direct event body (not stringified)."""
        event = {
            'repo_url': 'https://github.com/user/repo',
            'diagram_type': 'class',
            'output_format': 'mermaid'
        }
        
        with patch('src.handlers.main_handler.DiagramService') as mock_service_class:
            mock_service = Mock()
            mock_response = DiagramResponse(
                diagram_code="graph TD;\n    A[Test]",
                format=OutputFormat.MERMAID,
                metadata={},
                success=True
            )
            mock_service.generate_diagram.return_value = mock_response
            mock_service_class.return_value = mock_service
            
            response = lambda_handler(event, {})
            
            assert response['statusCode'] == 200
    
    def test_invalid_json_body(self):
        """Test handling of invalid JSON in body."""
        event = {
            'body': 'invalid json {'
        }
        
        response = lambda_handler(event, {})
        
        assert response['statusCode'] == 500
        body = json.loads(response['body'])
        assert 'Internal server error' in body['error']
    
    @patch('src.handlers.main_handler.DiagramService')
    def test_service_returns_error(self, mock_service_class):
        """Test handling when service returns error response."""
        # Mock service to return error response
        mock_service = Mock()
        mock_response = DiagramResponse(
            diagram_code="",
            format=OutputFormat.MERMAID,
            metadata={"error": "No source files found"},
            success=False,
            error="No source files found"
        )
        mock_service.generate_diagram.return_value = mock_response
        mock_service_class.return_value = mock_service
        
        event = {
            'body': json.dumps({
                'repo_url': 'https://github.com/user/empty-repo',
                'diagram_type': 'class',
                'output_format': 'mermaid'
            })
        }
        
        response = lambda_handler(event, {})
        
        # Should still return 200 but with success=False
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['success'] is False
        assert body['diagram_code'] == ""
    
    def test_options_request(self):
        """Test handling of CORS OPTIONS request."""
        event = {
            'httpMethod': 'OPTIONS'
        }
        
        response = lambda_handler(event, {})
        
        assert response['statusCode'] == 200
        assert 'Access-Control-Allow-Methods' in response['headers']
        assert 'Access-Control-Allow-Headers' in response['headers']