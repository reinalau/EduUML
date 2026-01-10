// File handling utilities for directory selection and processing

class FileHandler {
    constructor() {
        this.selectedFiles = new Map(); // Map of file path -> file content
        this.directoryPath = '';
    }

    /**
     * Initialize file input handlers
     */
    init() {
        const directoryInput = document.getElementById('directory-input');
        const selectButton = document.getElementById('select-directory-btn');

        selectButton.addEventListener('click', () => {
            directoryInput.click();
        });

        directoryInput.addEventListener('change', (event) => {
            this.handleDirectorySelection(event);
        });
    }

    /**
     * Handle directory selection from file input
     */
    async handleDirectorySelection(event) {
        const files = Array.from(event.target.files);
        
        if (files.length === 0) {
            this.clearSelection();
            return;
        }

        try {
            // Show loading state
            this.showLoadingState();

            // Process selected files
            await this.processFiles(files);

            // Update UI
            this.updateDirectoryDisplay(files);
            this.enableGenerateButton();

        } catch (error) {
            console.error('Error processing files:', error);
            this.showError('Error al procesar los archivos: ' + error.message);
        }
    }

    /**
     * Process and filter selected files
     */
    async processFiles(files) {
        this.selectedFiles.clear();
        
        console.log(`Processing ${files.length} total files`);
        console.log('Supported extensions:', CONFIG.SUPPORTED_EXTENSIONS);
        
        // Filter supported files
        const supportedFiles = files.filter(file => {
            const supported = this.isSupportedFile(file.name);
            if (!supported) {
                console.log(`Skipping unsupported file: ${file.name}`);
            }
            return supported;
        });

        console.log(`Found ${supportedFiles.length} supported files out of ${files.length} total`);

        if (supportedFiles.length === 0) {
            throw new Error('No se encontraron archivos de código fuente soportados');
        }

        if (supportedFiles.length > CONFIG.UI.MAX_TOTAL_FILES) {
            throw new Error(`Demasiados archivos. Máximo permitido: ${CONFIG.UI.MAX_TOTAL_FILES}`);
        }

        // Read file contents
        for (const file of supportedFiles) {
            if (file.size > CONFIG.UI.MAX_FILE_SIZE) {
                console.warn(`Archivo demasiado grande ignorado: ${file.name}`);
                continue;
            }

            try {
                const content = await this.readFileContent(file);
                const relativePath = this.getRelativePath(file.webkitRelativePath);
                this.selectedFiles.set(relativePath, content);
                console.log(`Added file: ${relativePath}`);
            } catch (error) {
                console.warn(`Error leyendo archivo ${file.name}:`, error);
            }
        }

        if (this.selectedFiles.size === 0) {
            throw new Error('No se pudieron leer los archivos seleccionados');
        }

        console.log(`Final selected files: ${this.selectedFiles.size}`);
        console.log('Selected file paths:', Array.from(this.selectedFiles.keys()));

        // Set directory path from first file
        if (supportedFiles.length > 0) {
            const firstFile = supportedFiles[0];
            this.directoryPath = this.extractDirectoryPath(firstFile.webkitRelativePath);
        }
    }

    /**
     * Check if file is supported based on extension
     */
    isSupportedFile(filename) {
        const extension = '.' + filename.split('.').pop().toLowerCase();
        const isSupported = CONFIG.SUPPORTED_EXTENSIONS.includes(extension);
        console.log(`Checking file: ${filename}, extension: ${extension}, supported: ${isSupported}`);
        return isSupported;
    }

    /**
     * Read file content as text
     */
    readFileContent(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = () => reject(new Error(`Error leyendo ${file.name}`));
            
            reader.readAsText(file, 'utf-8');
        });
    }

    /**
     * Get relative path from webkit relative path
     */
    getRelativePath(webkitPath) {
        // Remove the root directory name to get relative path
        const parts = webkitPath.split('/');
        return parts.slice(1).join('/');
    }

    /**
     * Extract directory path from webkit relative path
     */
    extractDirectoryPath(webkitPath) {
        const parts = webkitPath.split('/');
        return parts[0]; // First part is the root directory name
    }

    /**
     * Update directory display in UI
     */
    updateDirectoryDisplay(files) {
        const selectedPathElement = document.getElementById('selected-directory');
        const directoryInfoElement = document.getElementById('directory-info');
        const filesCountElement = document.getElementById('files-count');

        // Update selected path
        selectedPathElement.textContent = this.directoryPath || 'Directorio seleccionado';
        selectedPathElement.style.color = '#2d3748';
        selectedPathElement.style.fontStyle = 'normal';

        // Update file count
        const supportedCount = this.selectedFiles.size;
        const totalCount = files.length;
        
        filesCountElement.textContent = 
            `${supportedCount} archivos de código encontrados (${totalCount} archivos totales)`;

        // Show directory info
        directoryInfoElement.style.display = 'block';
    }

    /**
     * Show loading state during file processing
     */
    showLoadingState() {
        const selectedPathElement = document.getElementById('selected-directory');
        selectedPathElement.textContent = 'Procesando archivos...';
        selectedPathElement.style.color = '#718096';
        selectedPathElement.style.fontStyle = 'italic';
    }

    /**
     * Clear file selection
     */
    clearSelection() {
        this.selectedFiles.clear();
        this.directoryPath = '';

        const selectedPathElement = document.getElementById('selected-directory');
        const directoryInfoElement = document.getElementById('directory-info');

        selectedPathElement.textContent = 'Ningún directorio seleccionado';
        selectedPathElement.style.color = '#666';
        selectedPathElement.style.fontStyle = 'italic';

        directoryInfoElement.style.display = 'none';

        this.disableGenerateButton();
    }

    /**
     * Enable generate button
     */
    enableGenerateButton() {
        if (window.umlApp) {
            window.umlApp.updateGenerateButtonState();
        } else {
            const generateBtn = document.getElementById('generate-btn');
            generateBtn.disabled = false;
        }
    }

    /**
     * Disable generate button
     */
    disableGenerateButton() {
        const generateBtn = document.getElementById('generate-btn');
        generateBtn.disabled = true;
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
     * Get selected files as object for API request
     */
    getSelectedFilesObject() {
        const filesObject = {};
        for (const [path, content] of this.selectedFiles) {
            filesObject[path] = content;
        }
        return filesObject;
    }

    /**
     * Get directory info for metadata
     */
    getDirectoryInfo() {
        return {
            path: this.directoryPath,
            fileCount: this.selectedFiles.size,
            extensions: this.getFileExtensions()
        };
    }

    /**
     * Get unique file extensions from selected files
     */
    getFileExtensions() {
        const extensions = new Set();
        for (const path of this.selectedFiles.keys()) {
            const ext = '.' + path.split('.').pop().toLowerCase();
            extensions.add(ext);
        }
        return Array.from(extensions);
    }

    /**
     * Check if files are selected
     */
    hasFiles() {
        return this.selectedFiles.size > 0;
    }
}

// Create global instance
const fileHandler = new FileHandler();