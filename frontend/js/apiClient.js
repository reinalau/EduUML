// API client for communicating with the UML Diagram Generator backend

class ApiClient {
    constructor() {
        this.baseUrl = CONFIG.API.BASE_URL;
        this.timeout = CONFIG.API.TIMEOUT;
    }

    /**
     * Generate diagram by calling the backend API
     */
    async generateDiagram(request) {
        const url = `${this.baseUrl}${CONFIG.API.ENDPOINTS.GENERATE_DIAGRAM}`;
        
        try {
            console.log('Sending request to:', url);
            console.log('Request payload:', request);

            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), this.timeout);

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(request),
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(
                    errorData.error || 
                    `HTTP ${response.status}: ${response.statusText}`
                );
            }

            const result = await response.json();
            console.log('API Response:', result);

            return result;

        } catch (error) {
            console.error('API Error:', error);
            
            if (error.name === 'AbortError') {
                throw new Error('La solicitud tardó demasiado tiempo. Intenta con menos archivos.');
            }
            
            if (error.message.includes('Failed to fetch')) {
                throw new Error('No se pudo conectar con el servidor. Verifica que esté ejecutándose.');
            }

            throw error;
        }
    }

    /**
     * Build request object from form data
     */
    buildRequest(formData, files) {
        const request = {
            // Use code_files for direct file content
            code_files: files,
            diagram_type: formData.diagramType,
            output_format: formData.outputFormat,
            analysis_method: formData.analysisMethod,
            filters: {}
        };

        return request;
    }

    /**
     * Test API connection
     */
    async testConnection() {
        try {
            const testRequest = {
                code_files: {
                    'test.py': 'class TestClass:\n    def test_method(self):\n        pass'
                },
                diagram_type: 'class',
                output_format: 'mermaid',
                analysis_method: 'llm_direct'
            };

            await this.generateDiagram(testRequest);
            return true;
        } catch (error) {
            console.error('Connection test failed:', error);
            return false;
        }
    }

    /**
     * Set API base URL (for configuration)
     */
    setBaseUrl(url) {
        this.baseUrl = url.replace(/\/$/, ''); // Remove trailing slash
    }

    /**
     * Get current API base URL
     */
    getBaseUrl() {
        return this.baseUrl;
    }
}

// Create global instance
const apiClient = new ApiClient();