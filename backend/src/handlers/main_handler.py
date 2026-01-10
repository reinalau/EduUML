"""Main Lambda handler for UML diagram generation."""

import json
import logging
import traceback
from typing import Dict, Any
from ..services.diagram_service import DiagramService
from ..models import AnalysisRequest, DiagramType, OutputFormat, AnalysisMethod

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda handler for processing UML diagram generation requests.
    
    Args:
        event: Lambda event containing request data
        context: Lambda context object
        
    Returns:
        HTTP response with generated diagram or error
    """
    try:
        # Log incoming request
        logger.info(f"Received request: {json.dumps(event, default=str)}")
        
        # Handle CORS preflight OPTIONS requests
        http_method = event.get('httpMethod') or event.get('requestContext', {}).get('http', {}).get('method')
        if http_method == 'OPTIONS':
            return handle_options_request()
        
        # Parse request body
        if 'body' in event and event['body']:
            if isinstance(event['body'], str):
                body = json.loads(event['body'])
            else:
                body = event['body']
        else:
            body = event
        
        # Validate required fields - at least one source must be provided
        has_repo = 'repo_url' in body and body['repo_url']
        has_local_dir = 'local_directory' in body and body['local_directory']
        has_code_files = 'code_files' in body and body['code_files']
        
        if not (has_repo or has_local_dir or has_code_files):
            return create_error_response(
                400, 
                "At least one source must be provided: repo_url, local_directory, or code_files"
            )
        
        # Validate other required fields
        required_fields = ['diagram_type', 'output_format']
        missing_fields = [field for field in required_fields if field not in body]
        
        if missing_fields:
            return create_error_response(
                400, 
                f"Missing required fields: {', '.join(missing_fields)}"
            )
        
        # Create analysis request
        try:
            request = AnalysisRequest(
                repo_url=body.get('repo_url'),
                local_directory=body.get('local_directory'),
                code_files=body.get('code_files'),
                diagram_type=DiagramType(body['diagram_type']),
                output_format=OutputFormat(body['output_format']),
                analysis_method=AnalysisMethod(body.get('analysis_method', 'llm_direct')),
                filters=body.get('filters', {})
            )
        except ValueError as e:
            return create_error_response(400, f"Invalid request parameters: {str(e)}")
        
        # Process request
        service = DiagramService()
        result = service.generate_diagram(request)
        
        # Return success response
        return create_success_response({
            'diagram_code': result.diagram_code,
            'format': result.format.value,
            'metadata': result.metadata,
            'success': result.success
        })
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        return create_error_response(
            500, 
            f"Internal server error: {str(e)}"
        )


def create_success_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a successful HTTP response."""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(data)
    }


def create_error_response(status_code: int, message: str) -> Dict[str, Any]:
    """Create an error HTTP response."""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps({
            'error': message,
            'success': False
        })
    }


def handle_options_request() -> Dict[str, Any]:
    """Handle CORS preflight OPTIONS requests."""
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '86400'
        },
        'body': ''
    }