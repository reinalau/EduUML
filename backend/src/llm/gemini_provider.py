"""Google Gemini LLM provider - Updated to use google.genai."""

from google import genai
from google.genai import types
import os
from typing import Dict
import logging
from ..models import DiagramType, OutputFormat
from ..prompts import DIAGRAM_PROMPTS

logger = logging.getLogger(__name__)


class GeminiProvider:
    """Google Gemini LLM provider using google.genai."""
    
    def __init__(self):
        # API Key from environment variables
        self.api_key = os.getenv("GOOGLE_API_KEY")
        logger.info(f"API Key loaded: {'Yes' if self.api_key else 'No'}")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
        self.model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")
        logger.info(f"Model name: {self.model_name}")
        
        # Initialize Gemini client
        self.client = genai.Client(api_key=self.api_key)

           
        # Load prompts from prompts.py file
        self.custom_prompts = {
            DiagramType.USE_CASE: DIAGRAM_PROMPTS.get("use_case", ""),
            DiagramType.SEQUENCE: DIAGRAM_PROMPTS.get("sequence", ""),
            DiagramType.ACTIVITY: DIAGRAM_PROMPTS.get("activity", ""),
            DiagramType.CLASS: DIAGRAM_PROMPTS.get("class", ""),
            DiagramType.COMPONENT: DIAGRAM_PROMPTS.get("component", ""),
            DiagramType.DEPLOYMENT: DIAGRAM_PROMPTS.get("deployment", ""),
            DiagramType.STATE: DIAGRAM_PROMPTS.get("state", ""),
        }
        logger.info(f"Prompts loaded: {len(self.custom_prompts)} prompts available")
    
    def generate_diagram_from_github_url(self, 
                                        repo_url: str,
                                        diagram_type: DiagramType,
                                        output_format: OutputFormat) -> tuple[str, str]:
        """Generate diagram from GitHub repository URL - returns (diagram_code, metadata)."""
        try:
            # Get custom prompt for diagram type
            custom_prompt = self.custom_prompts.get(diagram_type, "")
            if not custom_prompt:
                custom_prompt = self._get_default_prompt(diagram_type, output_format)
            
            # Replace {format_diagram} parameter
            format_name = self._get_format_name(output_format)
            custom_prompt = custom_prompt.replace("{format_diagram}", format_name)
            
            # Build parts list with the GitHub URL
            parts = []
            
            # Add the main prompt
            parts.append(types.Part.from_text(text=custom_prompt))
            
            # Add the GitHub URL as a separate part
            parts.append(types.Part.from_text(text=f"Repositorio de GitHub: {repo_url}"))
            
            # Define response schema for structured JSON output
            response_schema = types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "metadata": types.Schema(type=types.Type.STRING),
                    "codigoUML": types.Schema(type=types.Type.STRING),
                },
                required=["metadata", "codigoUML"]
            )
            
            generate_content_config = types.GenerateContentConfig(
                temperature=0,
                response_mime_type="application/json",
                response_schema=response_schema,
                thinking_config = types.ThinkingConfig(
                    thinking_budget=-1,
                ),
            )

            # Generate response using the new API with structured JSON output
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=types.Content(role="user", parts=parts),
                config=generate_content_config,
            )
            
            if not response.text:
                raise ValueError("Empty response from Gemini")
            
            # Parse JSON response - now guaranteed to be valid JSON
            try:
                import json
                response_text = response.text.strip()
                
                # Parse JSON directly (guaranteed valid by Gemini's response_mime_type)
                parsed_response = json.loads(response_text)
                
                # Extract codigoUML and metadata
                metadata = parsed_response.get("metadata", "")
                codigo_uml = parsed_response.get("codigoUML", "")
                
                # Unescape literal \n, \t, \r sequences to actual characters
                codigo_uml = codigo_uml.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r')
                
                # Sanitize diagram code (remove markdown code block markers)
                codigo_uml = self._sanitize_diagram_code(codigo_uml, output_format)
                
                logger.info(f"Successfully parsed JSON response from GitHub URL. Metadata length: {len(metadata)}, Code length: {len(codigo_uml)}")
                
                # Return both diagram code and metadata
                if not codigo_uml:
                    logger.warning(f"No 'codigoUML' field found in parsed JSON. Response keys: {parsed_response.keys()}")
                return codigo_uml, metadata
                    
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {str(e)}. Response text: {response_text}")
                return "", ""
            
        except Exception as e:
            logger.error(f"Error in Gemini generation from GitHub URL: {str(e)}")
            raise RuntimeError(f"Gemini generation failed: {str(e)}")
    
    def generate_diagram_from_source_files(self, 
                                          source_files: Dict[str, str], 
                                          diagram_type: DiagramType,
                                          output_format: OutputFormat) -> tuple[str, str]:
        """Generate diagram - returns (diagram_code, metadata)."""
        try:
            # Get custom prompt for diagram type
            custom_prompt = self.custom_prompts.get(diagram_type, "")
            if not custom_prompt:
                custom_prompt = self._get_default_prompt(diagram_type, output_format)
            
            # Replace {format_diagram} parameter
            format_name = self._get_format_name(output_format)
            custom_prompt = custom_prompt.replace("{format_diagram}", format_name)
            
            # Build parts list like in pruebaGemini.py
            parts = []
            
            # Add the main prompt
            parts.append(types.Part.from_text(text=custom_prompt))
            
            # Add each source file as a separate part
            for file_path, content in source_files.items():
                if content.strip():
                    parts.append(types.Part.from_text(text=f"--- FILE: {file_path} ---\n{content}"))
            
            # Define response schema for structured JSON output
            response_schema = types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "metadata": types.Schema(type=types.Type.STRING),
                    "codigoUML": types.Schema(type=types.Type.STRING),
                },
                required=["metadata", "codigoUML"]
            )
            
            generate_content_config = types.GenerateContentConfig(
                temperature=0,
                response_mime_type="application/json",
                response_schema=response_schema,
                thinking_config = types.ThinkingConfig(
                    thinking_budget=-1,
                ),
            )

            # Generate response using the new API with structured JSON output
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=types.Content(role="user", parts=parts),
                config=generate_content_config,
            )
            
            if not response.text:
                raise ValueError("Empty response from Gemini")
            
            # Parse JSON response - now guaranteed to be valid JSON
            try:
                import json
                response_text = response.text.strip()
                
                # Parse JSON directly (guaranteed valid by Gemini's response_mime_type)
                parsed_response = json.loads(response_text)
                
                # Extract codigoUML and metadata
                metadata = parsed_response.get("metadata", "")
                codigo_uml = parsed_response.get("codigoUML", "")
                
                # Unescape literal \n, \t, \r sequences to actual characters
                codigo_uml = codigo_uml.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r')
                
                # Sanitize diagram code (remove markdown code block markers)
                codigo_uml = self._sanitize_diagram_code(codigo_uml, output_format)
                
                logger.info(f"Successfully parsed JSON response. Metadata length: {len(metadata)}, Code length: {len(codigo_uml)}")
                
                # Return both diagram code and metadata
                if not codigo_uml:
                    logger.warning(f"No 'codigoUML' field found in parsed JSON. Response keys: {parsed_response.keys()}")
                return codigo_uml, metadata
                    
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {str(e)}. Response text: {response_text}")
                return "", ""
            
        except Exception as e:
            logger.error(f"Error in Gemini generation: {str(e)}")
            raise RuntimeError(f"Gemini generation failed: {str(e)}")
    
    def _get_format_name(self, output_format: OutputFormat) -> str:
        """Get format name for prompt substitution."""
        format_names = {
            OutputFormat.DRAWIO: "Draw.io",
            OutputFormat.PLANTUML: "PlantUML", 
            OutputFormat.MERMAID: "Mermaid"
        }
        return format_names.get(output_format, output_format.value)
    
    def _get_default_prompt(self, diagram_type: DiagramType, output_format: OutputFormat) -> str:
        """Get default prompt when custom prompt is not available."""
        format_name = self._get_format_name(output_format)
        return f"""Actúa como un arquitecto de software senior y profesor de ingeniería. 
               Analiza el siguiente código fuente proporcionado y genera un diagrama UML de tipo {diagramType}.
               REQUISITOS:
                1. Genera código {format_name} funcional para el diagrama.
                2. Proporciona una explicación educativa clara de lo que muestra el diagrama, los patrones encontrados y las relaciones principales.
                Responde exclusivamente en formato JSON con la siguiente estructura:
                {{
                    "metadata": "Explicación detallada en español para estudiantes",
                    "codigoUML": "código {format_name} aquí"
                }}"""



    def _sanitize_diagram_code(self, code: str, output_format: OutputFormat) -> str:
        """Remove markdown code block markers from diagram code."""
        if not code:
            return code
        
        # Get the format language identifier
        format_lang = output_format.value.lower()  # 'mermaid', 'drawio', 'plantuml'
        
        # Remove opening backticks with language specifier: ```language\n
        opening_marker = f"```{format_lang}\n"
        if code.startswith(opening_marker):
            code = code[len(opening_marker):]
        
        # Remove closing backticks: ```
        if code.endswith("```"):
            code = code[:-3]
        
        return code