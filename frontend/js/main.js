// Main application logic and event handlers

class UMLDiagramApp {
    constructor() {
        this.isGenerating = false;
        this.currentResult = null;
    }

    /**
     * Initialize the application
     */
    init() {
        console.log('Initializing UML Diagram Generator...');
        
        // Initialize components
        fileHandler.init();
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Initialize Mermaid
        this.initializeMermaid();
        
        console.log('Application initialized successfully');
    }

    /**
     * Setup all event listeners
     */
    setupEventListeners() {
        // Source type radio buttons
        document.querySelectorAll('input[name="source-type"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.handleSourceTypeChange(e.target.value);
            });
        });

        // GitHub URL input
        const githubUrlInput = document.getElementById('github-url-input');
        if (githubUrlInput) {
            githubUrlInput.addEventListener('input', () => {
                this.updateGenerateButtonState();
            });
        }

        // Generate button
        document.getElementById('generate-btn').addEventListener('click', () => {
            this.handleGenerateClick();
        });

        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });

        // Copy code button
        document.getElementById('copy-code-btn').addEventListener('click', () => {
            this.copyCodeToClipboard();
        });

        // Download code button
        document.getElementById('download-code-btn').addEventListener('click', () => {
            this.downloadCode();
        });

        // Error dismiss button
        document.getElementById('dismiss-error-btn').addEventListener('click', () => {
            this.hideError();
        });

        // Form change handlers
        document.getElementById('output-format').addEventListener('change', () => {
            this.updateFormatDescription();
        });

        document.getElementById('diagram-type').addEventListener('change', () => {
            this.updateDiagramDescription();
        });
    }

    /**
     * Handle source type change (Local vs GitHub)
     */
    handleSourceTypeChange(sourceType) {
        const localSection = document.getElementById('local-source-section');
        const githubSection = document.getElementById('github-source-section');
        
        if (sourceType === 'local') {
            localSection.style.display = 'block';
            githubSection.style.display = 'none';
            this.updateGenerateButtonState();
        } else if (sourceType === 'github') {
            localSection.style.display = 'none';
            githubSection.style.display = 'block';
            this.updateGenerateButtonState();
        }
    }

    /**
     * Get the currently selected source type
     */
    getSourceType() {
        return document.querySelector('input[name="source-type"]:checked').value;
    }

    /**
     * Initialize Mermaid library
     */
    initializeMermaid() {
        if (typeof mermaid !== 'undefined') {
            mermaid.initialize({
                startOnLoad: false,
                theme: 'default',
                securityLevel: 'loose'
            });
            console.log('Mermaid initialized');
        } else {
            console.warn('Mermaid library not loaded');
        }
    }

    /**
     * Handle generate button click
     */
    async handleGenerateClick() {
        if (this.isGenerating) {
            return;
        }

        const sourceType = this.getSourceType();

        if (sourceType === 'local') {
            await this.handleGenerateFromLocal();
        } else if (sourceType === 'github') {
            await this.handleGenerateFromGitHub();
        }
    }

    /**
     * Handle generation from local directory
     */
    async handleGenerateFromLocal() {
        if (!fileHandler.hasFiles()) {
            this.showError('Por favor selecciona un directorio con archivos de código fuente');
            return;
        }

        try {
            this.setGeneratingState(true);
            this.hideError();

            // Get form data
            const formData = this.getFormData();
            
            // Get selected files
            const files = fileHandler.getSelectedFilesObject();
            
            // Build API request
            const request = apiClient.buildRequest(formData, files);
            
            // Call API
            const result = await apiClient.generateDiagram(request);
            
            // Handle response
            await this.handleGenerationResult(result);
            
        } catch (error) {
            console.error('Generation error:', error);
            this.showError(error.message);
        } finally {
            this.setGeneratingState(false);
        }
    }

    /**
     * Handle generation from GitHub URL
     */
    async handleGenerateFromGitHub() {
        const githubUrl = document.getElementById('github-url-input').value.trim();
        
        if (!githubUrl || !githubUrl.includes('github.com')) {
            this.showError('Por favor ingresa una URL válida de GitHub');
            return;
        }

        try {
            this.setGeneratingState(true);
            this.hideError();
            
            const formData = this.getFormData();
            const request = {
                repo_url: githubUrl,
                diagram_type: formData.diagramType,
                output_format: formData.outputFormat,
                analysis_method: formData.analysisMethod,
                filters: {}
            };
            
            const result = await apiClient.generateDiagram(request);
            await this.handleGenerationResult(result);
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.setGeneratingState(false);
        }
    }

    /**
     * Get form data from UI
     */
    getFormData() {
        return {
            analysisMethod: document.querySelector('input[name="analysis-method"]:checked').value,
            outputFormat: document.getElementById('output-format').value,
            diagramType: document.getElementById('diagram-type').value
        };
    }

    /**
     * Handle generation result
     */
    async handleGenerationResult(result) {
        if (!result.success) {
            throw new Error(result.error || 'Error desconocido en la generación');
        }

        this.currentResult = result;

        // Show results panel
        this.showResultsPanel();

        // Update code view
        this.updateCodeView(result.diagram_code);

        // Update metadata view
        this.updateMetadataView(result.metadata);

        // Render diagram
        await diagramRenderer.renderDiagram(result.diagram_code, result.format);

        // Switch to viewer tab
        this.switchTab('viewer');

        console.log('Diagram generated successfully');
    }

    /**
     * Set generating state
     */
    setGeneratingState(isGenerating) {
        this.isGenerating = isGenerating;
        
        const generateBtn = document.getElementById('generate-btn');
        const generateText = document.getElementById('generate-text');
        const loadingSpinner = document.getElementById('loading-spinner');

        if (isGenerating) {
            generateBtn.disabled = true;
            generateText.style.display = 'none';
            loadingSpinner.style.display = 'inline';
        } else {
            // Re-enable button based on current source type
            this.updateGenerateButtonState();
            generateText.style.display = 'inline';
            loadingSpinner.style.display = 'none';
        }
    }

    /**
     * Show results panel
     */
    showResultsPanel() {
        const resultsPanel = document.getElementById('results-panel');
        resultsPanel.style.display = 'block';
        // Hide initial welcome viewport when showing results
        const initial = document.getElementById('initial-viewport');
        if (initial) initial.style.display = 'none';

        // Scroll to results
        resultsPanel.scrollIntoView({ behavior: 'smooth' });
    }

    /**
     * Switch between tabs
     */
    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');
    }

    /**
     * Update code view
     */
    updateCodeView(code) {
        const codeElement = document.getElementById('diagram-code');
        codeElement.textContent = code;
    }

    /**
     * Update metadata view
     */
    updateMetadataView(metadata) {
        const metadataContent = document.getElementById('metadata-content');
        
        let html = '<h4>Información de Generación</h4>';
        
        if (metadata.source) {
            html += `<p><strong>Fuente:</strong> ${metadata.source.type || 'Archivos locales'}</p>`;
        }
        
        if (metadata.files_analyzed) {
            html += `<p><strong>Archivos analizados:</strong> ${metadata.files_analyzed}</p>`;
        }
        
        if (metadata.analysis_method) {
            html += `<p><strong>Método de análisis:</strong> ${metadata.analysis_method}</p>`;
        }
        
        if (metadata.llm_provider) {
            html += `<p><strong>Proveedor LLM:</strong> ${metadata.llm_provider}</p>`;
        }
        
        if (metadata.languages && metadata.languages.length > 0) {
            html += `<p><strong>Lenguajes detectados:</strong> ${metadata.languages.join(', ')}</p>`;
        }
        
        if (metadata.elements_found) {
            html += `<p><strong>Elementos encontrados:</strong> ${metadata.elements_found}</p>`;
        }

        // Add LLM Analysis section if available
        if (metadata.llm_metadata && metadata.llm_metadata.trim()) {
            html += `
                <div class="analysis-section">
                    <h4>📝 Análisis del LLM</h4>
                    <div style="position: relative;">
                        <button id="copy-analysis-btn">📋 Copiar Análisis</button>
                        <div id="llm-analysis-content">${this.escapeHtml(metadata.llm_metadata)}</div>
                    </div>
                </div>
            `;
        }

        metadataContent.innerHTML = html;

        // Add event listener for copy analysis button if it exists
        const copyAnalysisBtn = document.getElementById('copy-analysis-btn');
        if (copyAnalysisBtn) {
            copyAnalysisBtn.addEventListener('click', () => {
                this.copyAnalysisToClipboard(metadata.llm_metadata);
            });
        }
    }

    /**
     * Copy code to clipboard
     */
    async copyCodeToClipboard() {
        if (!this.currentResult) {
            return;
        }

        try {
            await navigator.clipboard.writeText(this.currentResult.diagram_code);
            this.showTemporaryMessage('Código copiado al portapapeles');
        } catch (error) {
            console.error('Error copying to clipboard:', error);
            this.showError('Error copiando al portapapeles');
        }
    }

    /**
     * Copy LLM analysis to clipboard
     */
    async copyAnalysisToClipboard(analysisText) {
        if (!analysisText) {
            return;
        }

        try {
            await navigator.clipboard.writeText(analysisText);
            this.showTemporaryMessage('Análisis copiado al portapapeles');
        } catch (error) {
            console.error('Error copying analysis to clipboard:', error);
            this.showError('Error copiando análisis al portapapeles');
        }
    }

    /**
     * Escape HTML characters for safe display
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Download code as file
     */
    downloadCode() {
        if (!this.currentResult) {
            return;
        }

        const format = this.currentResult.format;
        const code = this.currentResult.diagram_code;
        const extension = CONFIG.OUTPUT_FORMATS[format].extension;
        
        const blob = new Blob([code], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `diagram${extension}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        URL.revokeObjectURL(url);
        
        this.showTemporaryMessage('Archivo descargado');
    }

    /**
     * Show error message
     */
    showError(message) {
        const errorPanel = document.getElementById('error-panel');
        const errorMessage = document.getElementById('error-message');
        
        errorMessage.textContent = message;
        errorPanel.style.display = 'block';
        
        // Scroll to error
        errorPanel.scrollIntoView({ behavior: 'smooth' });
    }

    /**
     * Hide error message
     */
    hideError() {
        const errorPanel = document.getElementById('error-panel');
        errorPanel.style.display = 'none';
    }

    /**
     * Show temporary success message
     */
    showTemporaryMessage(message) {
        // Create temporary message element
        const messageEl = document.createElement('div');
        messageEl.textContent = message;
        messageEl.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #48bb78;
            color: white;
            padding: 12px 20px;
            border-radius: 6px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            font-weight: 500;
        `;
        
        document.body.appendChild(messageEl);
        
        // Remove after 3 seconds
        setTimeout(() => {
            if (messageEl.parentNode) {
                messageEl.parentNode.removeChild(messageEl);
            }
        }, 3000);
    }

    /**
     * Update format description (future enhancement)
     */
    updateFormatDescription() {
        // Could add format descriptions in the UI
    }

    /**
     * Update diagram description (future enhancement)
     */
    updateDiagramDescription() {
        // Could add diagram type descriptions in the UI
    }

    /**
     * Update generate button state based on source type and input validation
     */
    updateGenerateButtonState() {
        const generateBtn = document.getElementById('generate-btn');
        const sourceType = this.getSourceType();
        let isValid = false;

        if (sourceType === 'local') {
            isValid = fileHandler.hasFiles();
        } else if (sourceType === 'github') {
            const githubUrl = document.getElementById('github-url-input').value.trim();
            isValid = githubUrl && githubUrl.includes('github.com');
        }

        generateBtn.disabled = !isValid;
    }
}

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const app = new UMLDiagramApp();
    app.init();
});

// Make app available globally for debugging
window.umlApp = new UMLDiagramApp();