import os
from google import genai
from google.genai import types

client = genai.Client(api_key="xxxx")

def get_code_context(directory):
    parts = []
    # Instrucción inicial
    format_diagram= "MERMAID"
    prompt=f"""Actúa como un arquitecto de software senior y profesor de ingeniería. Analiza el código fuente adjunto y genera un diagrama UML de Clases. 
                REQUISITOS:
                a-Genera código {format_diagram} funcional para el diagrama. 
                b-Proporciona una explicación educativa clara de lo que muestra el diagrama, los patrones encontrados y las relaciones principales.
                c-Responde exclusivamente en formato JSON con la siguiente estructura: 
                {{
                "metadata": "Explicación detallada en español para estudiantes",
                "codigoUML": "código plantuml {format_diagram} aquí"
                }}"""
    parts.append(types.Part.from_text(text=prompt))
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.py', '.js', '.ts', '.java', '.cpp')): # Filtra tus extensiones
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Enviamos cada archivo como una "Part" de texto identificada
                    parts.append(types.Part.from_text(text=f"--- FILE: {file} ---\n{content}"))
    return parts

# Ejecución
project_path = "C:/Users/nn/Documents/...."
project_parts = get_code_context(project_path)

#response = client.models.generate_content(
#    model="gemini-2.5-flash",
#    contents=types.Content(role="user", parts=project_parts)
#)
generate_content_config = types.GenerateContentConfig(
        temperature=0.2,
        thinking_config = types.ThinkingConfig(
            thinking_budget=-1,
        ),
       
)

for chunk in client.models.generate_content_stream(
        model="gemini-2.5-flash-lite",  #"gemini-2.5-flash",
        contents=types.Content(role="user", parts=project_parts),
        config=generate_content_config,
):
    print(chunk.text, end="")

