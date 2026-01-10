// Configuration settings for the UML Diagram Generator

const CONFIG = {
    // API Configuration
    API: {
        // Default to local development, can be overridden
        BASE_URL: 'http://127.0.0.1:3000',
        ENDPOINTS: {
            GENERATE_DIAGRAM: '/generate-diagram'
        },
        TIMEOUT: 300000 // timeout para generación de diagramas
    },

    // Supported file extensions for source code analysis
    SUPPORTED_EXTENSIONS: [
        '.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', 
        '.php', '.rb', '.go', '.kt', '.swift', '.rs', '.scala', 
        '.yaml', '.yml', '.tf', '.tfvars'
    ],

    // PlantUML server configuration
    PLANTUML: {
        SERVER_URL: 'http://www.plantuml.com/plantuml',
        // Alternative servers:
        // SERVER_URL: 'https://plantuml-server.kkeisuke.dev',
        // SERVER_URL: 'http://localhost:8080', // For local PlantUML server
        FORMAT: 'svg' // png, svg, txt
    },

    // Diagram type descriptions
    DIAGRAM_TYPES: {
        'class': {
            name: 'Diagrama de Clases',
            description: 'Muestra clases, atributos, métodos y relaciones entre ellas'
        },
        'sequence': {
            name: 'Diagrama de Secuencia', 
            description: 'Muestra interacciones entre actores y objetos en orden cronológico'
        },
        'use_case': {
            name: 'Diagrama de Casos de Uso',
            description: 'Muestra actores y casos de uso del sistema'
        },
        'activity': {
            name: 'Diagrama de Actividad',
            description: 'Muestra flujo de trabajo y control del sistema'
        },
        'component': {
            name: 'Diagrama de Componentes',
            description: 'Muestra módulos y sus interfaces'
        },
        'deployment': {
            name: 'Diagrama de Despliegue',
            description: 'Muestra nodos físicos y artefactos de software'
        },
        'state': {
            name: 'Diagrama de Estados',
            description: 'Muestra estados y transiciones de objetos'
        }
    },

    // Output format descriptions
    OUTPUT_FORMATS: {
        'drawio': {
            name: 'Draw.io (XML)',
            description: 'Compatible con Draw.io/Diagrams.net',
            extension: '.drawio'
        },
        'plantuml': {
            name: 'PlantUML',
            description: 'Compatible con PlantUML tools',
            extension: '.puml'
        },
        'mermaid': {
            name: 'Mermaid',
            description: 'Compatible con Mermaid.js',
            extension: '.mmd'
        }
    },

    // Analysis method descriptions
    ANALYSIS_METHODS: {
        'llm_direct': {
            name: 'AI Analysis (Gemini)',
            description: 'Análisis inteligente directo con LLM para mejores resultados'
        }
    },

    // UI Configuration
    UI: {
        MAX_FILE_SIZE: 1024 * 1024, // 1MB per file
        MAX_TOTAL_FILES: 100,
        ANIMATION_DURATION: 300
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}