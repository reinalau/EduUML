# Frontend Integration Notes

## Cambios Potenciales Necesarios en el Backend

### 1. CORS Configuration
**Estado**: ✅ SOLUCIONADO
**Descripción**: El frontend necesitará hacer requests desde el navegador al backend.
**Cambios realizados**:
- ✅ Agregado manejo de requests OPTIONS en `main_handler.py`
- ✅ Headers CORS configurados correctamente en todas las respuestas
- ✅ `Access-Control-Allow-Origin: *` configurado
- ✅ `Access-Control-Allow-Methods: POST, OPTIONS` configurado
- ✅ `Access-Control-Allow-Headers: Content-Type` configurado

### 2. API URL Configuration
**Estado**: ✅ SOLUCIONADO
**Descripción**: El frontend necesitaba la URL correcta del backend local
**Cambios realizados**:
- ✅ Actualizada URL en `frontend/js/config.js` de `localhost:3000` a `127.0.0.1:3000`
- ✅ Coincide con la URL del servidor SAM local

### 2. Request Format Validation
**Estado**: Verificar compatibilidad
**Descripción**: El frontend enviará requests con `code_files` en lugar de `local_directory`
**Request format del frontend**:
```json
{
  "code_files": {
    "path/file1.py": "contenido...",
    "path/file2.js": "contenido..."
  },
  "diagram_type": "class",
  "output_format": "drawio", 
  "analysis_method": "llm_direct"
}
```

**Verificar**: Que el backend maneje correctamente el campo `code_files` en lugar de `local_directory`.

### 3. Error Response Format
**Estado**: Verificar consistencia
**Descripción**: El frontend espera errores en formato específico
**Formato esperado**:
```json
{
  "success": false,
  "error": "mensaje de error",
  "diagram_code": "",
  "format": "drawio",
  "metadata": {}
}
```

### 4. Response Size Limits
**Estado**: Monitorear
**Descripción**: Los diagramas DrawIO pueden ser muy grandes (XML extenso)
**Consideraciones**:
- Verificar límites de respuesta de Lambda
- Considerar compresión si es necesario
- Monitorear timeouts para proyectos grandes

### 5. File Size and Count Limits
**Estado**: Implementar validación
**Descripción**: El frontend limita archivos pero el backend debería validar también
**Límites del frontend**:
- Máximo 100 archivos
- Máximo 1MB por archivo
- Solo extensiones soportadas

**Recomendación**: Agregar validación en el backend para estos límites.

### 6. Local Development Setup
**Estado**: Configurar
**Descripción**: Necesitamos ejecutar el backend localmente para desarrollo del frontend
**Opciones**:
1. SAM local: `sam local start-api`
2. Servidor de desarrollo Python simple
3. Configurar puerto y CORS para desarrollo local

### 7. PlantUML Server Integration
**Estado**: Verificar disponibilidad
**Descripción**: El frontend usa servidor público de PlantUML
**Consideraciones**:
- Verificar que el servidor público esté disponible
- Considerar servidor PlantUML local para desarrollo
- Manejar errores de conectividad del servidor PlantUML

### 8. Mermaid Diagram Validation
**Estado**: Verificar sintaxis
**Descripción**: Asegurar que los diagramas Mermaid generados sean válidos
**Verificar**:
- Sintaxis correcta de Mermaid en respuestas del LLM
- Caracteres especiales que puedan romper el rendering
- Formato de nodos y conexiones

### 9. DrawIO XML Format
**Estado**: Verificar compatibilidad
**Descripción**: Asegurar que el XML generado sea compatible con Draw.io
**Verificar**:
- Estructura XML correcta
- Elementos geométricos válidos
- Colores y estilos soportados

### 10. API Endpoint Configuration
**Estado**: Configurar
**Descripción**: El frontend necesita saber la URL del backend
**Configuración actual del frontend**:
```javascript
API: {
    BASE_URL: 'http://localhost:3000',
    ENDPOINTS: {
        GENERATE_DIAGRAM: '/generate-diagram'
    }
}
```

**Necesario**: Configurar la URL correcta según el deployment (local/AWS).

## Testing Checklist

### Backend API Testing
- [ ] Verificar CORS headers
- [ ] Probar request con `code_files`
- [ ] Verificar response format
- [ ] Probar todos los formatos de salida
- [ ] Probar todos los tipos de diagrama
- [ ] Probar ambos métodos de análisis

### Integration Testing
- [ ] Frontend puede conectar con backend local
- [ ] Requests se envían correctamente
- [ ] Responses se procesan correctamente
- [ ] Error handling funciona
- [ ] Diagramas se renderizan correctamente

### End-to-End Testing
- [ ] Seleccionar directorio funciona
- [ ] Generar diagrama funciona
- [ ] Cambiar formatos funciona
- [ ] Cambiar tipos de diagrama funciona
- [ ] Exportar/copiar funciona

## Deployment Notes

### Local Development
1. Ejecutar backend: `sam local start-api --port 3000`
2. Servir frontend: servidor HTTP simple en puerto 8080
3. Configurar CORS para desarrollo local

### Production Deployment
1. Deploy backend a AWS Lambda
2. Actualizar `CONFIG.API.BASE_URL` en frontend
3. Servir frontend desde S3 + CloudFront o servidor web
4. Configurar CORS para dominio de producción

## Próximos Pasos

1. **Probar integración local**: Ejecutar backend y frontend juntos
2. **Verificar CORS**: Asegurar que las requests funcionen desde el navegador
3. **Validar formatos**: Probar que todos los formatos se generen correctamente
4. **Optimizar performance**: Medir tiempos de respuesta con archivos reales
5. **Manejar errores**: Probar casos edge y manejo de errores
6. **Documentar deployment**: Crear guía de deployment completa