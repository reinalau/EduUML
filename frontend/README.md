# UML Diagram Generator - Frontend

Interfaz web para generar diagramas UML desde código fuente usando análisis AI (Gemini) o Tree-sitter.

## Características

- 📁 **Selección de Directorio**: Navega y selecciona directorios locales con código fuente
- 🤖 **Análisis AI**: Usa Gemini para análisis inteligente directo del código
- 🔧 **Análisis Tree-sitter**: Análisis tradicional con parsing estructural
- 📊 **Múltiples Formatos**: Genera diagramas en DrawIO, PlantUML y Mermaid
- 📋 **7 Tipos de Diagrama**: Clases, Secuencia, Casos de Uso, Actividad, Componentes, Despliegue, Estados
- 👁️ **Vista Previa**: Renderizado nativo de diagramas Mermaid y PlantUML
- 💾 **Exportación**: Boton derecha sobre el diagrama--> GuardarComo o abrir en nueva pestaña

## Tecnologías

- **HTML5**: Estructura semántica y File System Access API
- **CSS3**: Diseño responsive con Flexbox/Grid
- **JavaScript ES6+**: Lógica de aplicación modular
- **Mermaid.js**: Renderizado de diagramas Mermaid
- **PlantUML Server**: Renderizado de diagramas PlantUML

## Estructura del Proyecto

```
frontend/
├── index.html              # Página principal
├── styles/
│   └── main.css            # Estilos principales
├── js/
│   ├── config.js           # Configuración de la aplicación
│   ├── fileHandler.js      # Manejo de archivos y directorios
│   ├── apiClient.js        # Cliente API para backend
│   ├── diagramRenderer.js  # Renderizado de diagramas
│   └── main.js             # Lógica principal de la aplicación
└── README.md               # Este archivo
```

## Configuración

### Backend API
Configura la URL del backend en `js/config.js`:

```javascript
const CONFIG = {
    API: {
        BASE_URL: 'http://localhost:3000', // URL del backend
        ENDPOINTS: {
            GENERATE_DIAGRAM: '/generate-diagram'
        }
    }
};
```

### Extensiones Soportadas
El frontend filtra automáticamente estos tipos de archivo:
- Python: `.py`
- JavaScript: `.js`, `.ts`
- Java: `.java`
- C/C++: `.c`, `.cpp`
- C#: `.cs`
- PHP: `.php`
- Ruby: `.rb`
- Go: `.go`
- Kotlin: `.kt`
- Swift: `.swift`
- Rust: `.rs`
- Scala: `.scala`

## Uso

### 1. Seleccionar Directorio
- Haz clic en "Seleccionar Directorio"
- Navega y selecciona una carpeta con código fuente
- El sistema filtrará automáticamente archivos soportados

### 2. Configurar Generación
- **Método de Análisis**: Elige entre AI (Gemini) o Tree-sitter
- **Formato de Salida**: DrawIO, PlantUML o Mermaid
- **Tipo de Diagrama**: Selecciona el tipo de diagrama UML

### 3. Generar Diagrama
- Haz clic en "Generar Diagrama"
- Espera el procesamiento (puede tomar varios segundos)
- Revisa el resultado en las pestañas de Vista Previa, Código e Información

### 4. Exportar Resultado
- **Vista Previa**: Ve el diagrama renderizado
- **Código**: Copia o descarga el código del diagrama
- **Información**: Revisa metadatos de la generación

## Desarrollo Local

### 1. Ejecutar Backend
```bash
# En la carpeta raíz del proyecto
sam local start-api --port 3000
```

### 2. Servir Frontend
```bash
# Opción 1: Python
cd frontend
python -m http.server 8080

# Opción 2: Node.js
cd frontend
npx serve -p 8080

# Opción 3: PHP
cd frontend
php -S localhost:8080
```

### 3. Abrir en Navegador
Navega a `http://localhost:8080`

## Compatibilidad de Navegadores

### Requerido
- **File System Access API**: Chrome 86+, Edge 86+
- **ES6+ Features**: Chrome 60+, Firefox 60+, Safari 12+
- **Fetch API**: Todos los navegadores modernos

### Fallbacks
Para navegadores sin File System Access API, el sistema usa `<input type="file" webkitdirectory>` como fallback.

## Limitaciones

- **Tamaño de Archivo**: Máximo 1MB por archivo
- **Cantidad de Archivos**: Máximo 100 archivos por directorio
- **Navegadores**: Requiere navegadores modernos con soporte ES6+
- **CORS**: Requiere configuración CORS correcta en el backend

## Troubleshooting

### Error: "No se pudo conectar con el servidor"
- Verifica que el backend esté ejecutándose
- Revisa la URL en `js/config.js`
- Verifica configuración CORS del backend

### Error: "No se encontraron archivos soportados"
- Verifica que el directorio contenga archivos de código fuente
- Revisa las extensiones soportadas en `CONFIG.SUPPORTED_EXTENSIONS`

### Diagrama no se renderiza
- **Mermaid**: Verifica que la librería esté cargada
- **PlantUML**: Verifica conectividad con el servidor PlantUML
- **DrawIO**: Copia el XML y pégalo manualmente en Draw.io

### Performance lenta
- Reduce la cantidad de archivos seleccionados
- Usa archivos más pequeños
- Considera usar Tree-sitter en lugar de AI para proyectos grandes

## Próximas Mejoras

- [ ] Soporte para repositorios GitHub
- [ ] Editor de diagramas integrado
- [ ] Exportación como imagen
- [ ] Historial de diagramas generados
- [ ] Plantillas de diagramas personalizables
- [ ] Integración con IDEs populares

## Implementaciones
🔧 Cambios implementados:
1. JavaScript (diagramRenderer.js):
✅ Renderizado: Usa <img> en lugar de iframe
✅ URL: Cambiado a http://www.plantuml.com/plantuml/png/ (más confiable)
✅ Manejo de errores: onload/onerror más directo y elegante
✅ Estilos inline: maxWidth, maxHeight, objectFit: contain
✅ Exportación: Actualizada para buscar img en lugar de iframe
2. CSS (main.css):
✅ Contenedor: Mejor centrado con flexbox
✅ Imagen: Estilos responsive con object-fit: contain
✅ Padding: Agregado al contenedor para mejor espaciado
3. Ventajas de la nueva implementación:
🚀 Más rápido: Sin overhead de iframe
📱 Mejor responsive: object-fit: contain maneja mejor diferentes tamaños
🎨 Estilos más simples: Control directo sobre la imagen
🔧 Manejo de errores mejorado: Más directo y claro
💾 Exportación más confiable: Acceso directo a la imagen
La implementación ahora es más simple, eficiente y confiable. PlantUML debería renderizarse correctamente usando el método con <img> que es más estándar y fácil de mantener.


## Viewver Implementacion


✅ DrawIO Viewer implementado correctamente
Cambios realizados:
URL correcta: Usa encodeURIComponent + #R como en el ejemplo
Iframe funcional: Debería cargar el diagrama directamente
Fallback robusto: Si falla, muestra textarea con instrucciones
Enlace de respaldo: Para abrir en nueva pestaña
Método usado (del ejemplo):

```bash
const encoded = encodeURIComponent(code);
const viewerUrl = `https://viewer.diagrams.net/?lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram#R${encoded}
```

## Licencia

Este proyecto está bajo la licencia MIT.