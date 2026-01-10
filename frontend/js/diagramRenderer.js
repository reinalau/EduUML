// Diagram rendering utilities for different output formats

class DiagramRenderer {
    constructor() {
        this.currentFormat = null;
        this.currentCode = null;
    }

    /**
     * Render diagram based on format
     */
    async renderDiagram(diagramCode, format) {
        this.currentCode = diagramCode;
        this.currentFormat = format;

        // Hide all viewers first
        this.hideAllViewers();

        try {
            switch (format) {
                case 'mermaid':
                    await this.renderMermaid(diagramCode);
                    break;
                case 'plantuml':
                    await this.renderPlantUML(diagramCode);
                    break;
                case 'drawio':
                    this.renderDrawIO(diagramCode);
                    break;
                default:
                    throw new Error(`Formato no soportado: ${format}`);
            }
        } catch (error) {
            console.error('Error rendering diagram:', error);
            this.showRenderError(error.message);
        }
    }

    /**
     * Render Mermaid diagram
     */
    async renderMermaid(code) {
        const viewer = document.getElementById('mermaid-viewer');
        const container = document.getElementById('mermaid-diagram');
        
        try {
            // Clear previous content
            container.innerHTML = '';
            
            // Initialize Mermaid if not already done
            if (typeof mermaid !== 'undefined') {
                mermaid.initialize({ 
                    startOnLoad: false,
                    theme: 'default',
                    securityLevel: 'loose',
                    fontFamily: 'Arial, sans-serif'
                });

                // Generate unique ID for this diagram
                const diagramId = 'mermaid-' + Date.now();
                
                // Render the diagram
                const { svg } = await mermaid.render(diagramId, code);
                container.innerHTML = svg;
                
                // Show the viewer
                viewer.style.display = 'block';
            } else {
                throw new Error('Mermaid library not loaded');
            }
        } catch (error) {
            console.error('Mermaid rendering error:', error);
            container.innerHTML = `
                <div style="padding: 20px; text-align: center; color: #e53e3e;">
                    <h4>Error renderizando diagrama Mermaid</h4>
                    <p>${error.message}</p>
                    <p><small>Revisa la sintaxis del diagrama en la pestaña "Código"</small></p>
                </div>
            `;
            viewer.style.display = 'block';
        }
    }

    /**
     * Render PlantUML diagram
     */
    async renderPlantUML(code) {
        const viewer = document.getElementById('plantuml-viewer');
        
        try {
            // Use the working PlantUML encoding method with img
            const encoded = this.plantumlEncode(code);
            const imageUrl = `http://www.plantuml.com/plantuml/png/${encoded}`;
            
            // Show loading state
            viewer.innerHTML = '<div class="loading" style="padding: 20px; text-align: center; color: #666;">Generando diagrama...</div>';
            viewer.style.display = 'block';
            
            // Create image element with proper error handling
            const img = document.createElement('img');
            img.alt = 'Diagrama PlantUML';
            img.style.maxWidth = '100%';
            img.style.maxHeight = '100%';
            img.style.objectFit = 'contain';
            
            img.onload = function() {
                viewer.innerHTML = '';
                viewer.appendChild(img);
            };
            
            img.onerror = function() {
                viewer.innerHTML = `
                    <div style="padding: 20px; text-align: center; color: #e53e3e;">
                        <h4>⚠️ Error renderizando diagrama PlantUML</h4>
                        <p>Error al cargar el diagrama. Verifica la conexión o el código PlantUML.</p>
                        <p><strong>Código PlantUML:</strong></p>
                        <textarea readonly style="width: 100%; height: 200px; font-family: monospace; margin: 10px 0;">${code}</textarea>
                        <p>
                            <a href="http://www.plantuml.com/plantuml/uml" target="_blank" 
                               style="color: #0066cc; text-decoration: none;">
                                🔗 Abrir PlantUML Online y pegar el código manualmente
                            </a>
                        </p>
                    </div>
                `;
            };
            
            // Set source to start loading
            img.src = imageUrl;
            
        } catch (error) {
            console.error('PlantUML rendering error:', error);
            
            viewer.innerHTML = `
                <div style="padding: 20px; text-align: center; color: #e53e3e;">
                    <h4>❌ Error procesando código PlantUML</h4>
                    <p>${error.message}</p>
                    <p><strong>Código PlantUML:</strong></p>
                    <textarea readonly style="width: 100%; height: 200px; font-family: monospace; margin: 10px 0;">${code}</textarea>
                </div>
            `;
            viewer.style.display = 'block';
        }
    }

    /**
     * Render DrawIO diagram - fallback to textarea for now
     */
    renderDrawIO(code) {
        const viewer = document.getElementById('drawio-viewer');
        const textarea = document.getElementById('drawio-code');

        // Always keep a copy of the XML in the textarea for the "Código" tab
        if (textarea) textarea.value = code;

        try {
            // Encode XML for viewer.diagrams.net (use encodeURIComponent like the working example)
            const encoded = encodeURIComponent(code);
            const viewerUrl = `https://viewer.diagrams.net/?lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram#R${encoded}`;

            // Build embedded viewer with a link and an iframe; also provide the XML textarea below
            viewer.innerHTML = `
                <div style="margin-bottom: 15px; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; text-align: center;">
                    <h4 style="margin: 0 0 8px 0;">📊 Diagrama DrawIO Generado</h4>
                    <p style="margin: 0; opacity: 0.9;">Vista previa embebida usando Draw.io Viewer. Si hay problemas, abre en una nueva pestaña.</p>
                </div>
                <div style="margin-bottom:10px; display:flex; gap:10px; align-items:center;">
                    <div style="flex:1;">
                        <div class="url-info" style="margin-bottom:8px;">
                            <strong>Draw.io Viewer URL:</strong><br>
                            <a href="${viewerUrl}" target="_blank">Abrir en Draw.io Viewer</a>
                        </div>
                    </div>
                </div>
                <div style="height:420px; border:1px solid #e2e8f0; border-radius:6px; overflow:hidden;">
                    <iframe src="${viewerUrl}" style="width:100%; height:100%; border:0;" sandbox="allow-same-origin allow-scripts allow-forms allow-popups"></iframe>
                </div>
                <div style="margin-top:12px;">
                    <textarea readonly style="width: 100%; height: 200px; font-family: 'Courier New', monospace; font-size: 0.85rem; padding: 12px; border: 2px solid #e2e8f0; border-radius: 8px; background-color: #f8f9fa; line-height: 1.4; resize: vertical;">${code}</textarea>
                </div>
            `;

            viewer.style.display = 'block';
        } catch (err) {
            console.error('Error rendering DrawIO preview:', err);
            // Fallback: show textarea and instructions (preserves PlantUML and Mermaid behavior)
            viewer.innerHTML = `
                <div style="margin-bottom: 15px; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; text-align: center;">
                    <h4 style="margin: 0 0 8px 0;">📊 Diagrama DrawIO Generado</h4>
                    <p style="margin: 0; opacity: 0.9;">No se pudo generar la vista previa. Copia el código XML y pégalo en Draw.io.</p>
                </div>
                <textarea readonly style="width: 100%; height: 350px; font-family: 'Courier New', monospace; font-size: 0.85rem; padding: 15px; border: 2px solid #e2e8f0; border-radius: 8px; background-color: #f8f9fa; line-height: 1.4; resize: vertical;">${code}</textarea>
                <div style="margin-top: 15px; padding: 15px; background: #e6f3ff; border: 2px solid #0066cc; border-radius: 8px; display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 24px;">💡</span>
                    <div>
                        <strong>Cómo visualizar:</strong><br>
                        1. Selecciona y copia todo el código XML de arriba<br>
                        2. Ve a <a href="https://app.diagrams.net/" target="_blank" style="color: #0066cc; font-weight: bold;">Draw.io</a><br>
                        3. Archivo → Importar desde → Texto → Pega el código
                    </div>
                </div>
            `;

            viewer.style.display = 'block';
        }
    }

    /**
     * Hide all diagram viewers
     */
    hideAllViewers() {
        const viewers = [
            'mermaid-viewer',
            'plantuml-viewer', 
            'drawio-viewer'
        ];
        
        viewers.forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.style.display = 'none';
            }
        });
    }

    /**
     * Show render error
     */
    showRenderError(message) {
        // Find the currently visible viewer
        const mermaidViewer = document.getElementById('mermaid-viewer');
        const plantumlViewer = document.getElementById('plantuml-viewer');
        const drawioViewer = document.getElementById('drawio-viewer');
        
        let activeViewer = null;
        
        if (mermaidViewer && mermaidViewer.style.display !== 'none') {
            activeViewer = mermaidViewer;
        } else if (plantumlViewer && plantumlViewer.style.display !== 'none') {
            activeViewer = plantumlViewer;
        } else if (drawioViewer && drawioViewer.style.display !== 'none') {
            activeViewer = drawioViewer;
        }
        
        if (activeViewer) {
            activeViewer.innerHTML = `
                <div style="padding: 40px; text-align: center; color: #e53e3e;">
                    <h3>❌ Error de Renderizado</h3>
                    <p>${message}</p>
                    <p><small>Revisa el código generado en la pestaña "Código"</small></p>
                </div>
            `;
        }
    }

    /**
     * Encode PlantUML code using the working method (from plantuml-viewer.html)
     */
    plantumlEncode(text) {
        try {
            // Check if pako is available for compression
            if (typeof pako === 'undefined') {
                throw new Error('Librería pako no disponible para compresión PlantUML');
            }
            
            const data = new TextEncoder().encode(text);
            const compressed = pako.deflate(data, { level: 9 });
            const sliced = compressed.slice(2, -4);
            return this.encode64(sliced);
        } catch (error) {
            console.error('Error encoding PlantUML:', error);
            throw new Error('Error codificando diagrama PlantUML: ' + error.message);
        }
    }

    /**
     * PlantUML specific base64 encoding
     */
    encode64(data) {
        let r = '';
        for (let i = 0; i < data.length; i += 3) {
            if (i + 2 === data.length) {
                r += this.append3bytes(data[i], data[i + 1], 0);
            } else if (i + 1 === data.length) {
                r += this.append3bytes(data[i], 0, 0);
            } else {
                r += this.append3bytes(data[i], data[i + 1], data[i + 2]);
            }
        }
        return r;
    }

    /**
     * Helper function for PlantUML encoding
     */
    append3bytes(b1, b2, b3) {
        const c1 = b1 >> 2;
        const c2 = ((b1 & 0x3) << 4) | (b2 >> 4);
        const c3 = ((b2 & 0xF) << 2) | (b3 >> 6);
        const c4 = b3 & 0x3F;
        return this.encode6bit(c1 & 0x3F) + 
               this.encode6bit(c2 & 0x3F) + 
               this.encode6bit(c3 & 0x3F) + 
               this.encode6bit(c4 & 0x3F);
    }

    /**
     * Helper function for PlantUML encoding
     */
    encode6bit(b) {
        if (b < 10) return String.fromCharCode(48 + b);
        b -= 10;
        if (b < 26) return String.fromCharCode(65 + b);
        b -= 26;
        if (b < 26) return String.fromCharCode(97 + b);
        b -= 26;
        if (b === 0) return '-';
        if (b === 1) return '_';
        return '?';
    }

    /**
     * Export PlantUML diagram as image
     */
    async exportPlantUMLAsImage(format) {
        // Get the img element
        const img = document.querySelector('#plantuml-viewer img');
        if (!img || !img.src) {
            throw new Error('No hay diagrama PlantUML renderizado');
        }

        // Fetch the image and return as blob
        const response = await fetch(img.src);
        if (!response.ok) {
            throw new Error('Error descargando imagen PlantUML');
        }

        return await response.blob();
    }

    /**
     * Get current diagram code
     */
    getCurrentCode() {
        return this.currentCode;
    }

    /**
     * Get current format
     */
    getCurrentFormat() {
        return this.currentFormat;
    }

    /**
     * Export diagram as image (for supported formats)
     */
    async exportAsImage(format = 'png') {
        if (!this.currentCode || !this.currentFormat) {
            throw new Error('No hay diagrama para exportar');
        }

        switch (this.currentFormat) {
            case 'mermaid':
                return this.exportMermaidAsImage(format);
            case 'plantuml':
                return this.exportPlantUMLAsImage(format);
            case 'drawio':
                throw new Error('Exportar DrawIO como imagen no está soportado. Usa Draw.io para exportar.');
            default:
                throw new Error(`Exportar ${this.currentFormat} como imagen no está soportado`);
        }
    }

    /**
     * Export Mermaid diagram as image
     */
    async exportMermaidAsImage(format) {
        const svg = document.querySelector('#mermaid-diagram svg');
        if (!svg) {
            throw new Error('No hay diagrama Mermaid renderizado');
        }

        // Convert SVG to canvas and then to image
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();

        return new Promise((resolve, reject) => {
            img.onload = () => {
                canvas.width = img.width;
                canvas.height = img.height;
                ctx.drawImage(img, 0, 0);
                
                canvas.toBlob((blob) => {
                    if (blob) {
                        resolve(blob);
                    } else {
                        reject(new Error('Error generando imagen'));
                    }
                }, `image/${format}`);
            };
            
            img.onerror = () => reject(new Error('Error procesando SVG'));
            
            const svgData = new XMLSerializer().serializeToString(svg);
            const svgBlob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
            const url = URL.createObjectURL(svgBlob);
            img.src = url;
        });
    }
}

// Create global instance
const diagramRenderer = new DiagramRenderer();