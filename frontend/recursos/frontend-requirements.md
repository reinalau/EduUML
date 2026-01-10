# Frontend Web Interface for UML Diagram Generator

## Overview
Create a modern web interface for the UML Diagram Generator that allows users to analyze local source code directories and generate various types of UML diagrams using AI (Gemini) or Tree-sitter analysis.

## User Stories

### US1: Directory Selection
**As a user**, I want to select a local directory containing source code so that I can analyze my project structure.

**Acceptance Criteria:**
- Directory picker/browser component that allows navigation through local file system
- Display selected directory path clearly
- Show basic directory information (number of files, supported file types found)
- Support for common source code file extensions (.py, .js, .ts, .java, .cpp, .c, .cs, .php, .rb, .go)

### US2: Analysis Method Selection
**As a user**, I want to choose between AI analysis and Tree-sitter analysis so that I can select the most appropriate method for my needs.

**Acceptance Criteria:**
- Radio button or toggle selection between:
  - **AI Analysis (Gemini)**: Direct LLM analysis for intelligent diagram generation
- Clear explanation of each method's benefits and use cases
- Default to AI Analysis for better user experience

### US3: Output Format Selection
**As a user**, I want to choose the diagram output format so that I can use it with my preferred tools.

**Acceptance Criteria:**
- Dropdown or radio button selection for:
  - **DrawIO**: For use with Draw.io/Diagrams.net
  - **PlantUML**: For PlantUML tools and editors
  - **Mermaid**: For Mermaid.js integration
- Format descriptions and use cases displayed
- Default to DrawIO format

### US4: Diagram Type Selection
**As a user**, I want to select the type of UML diagram to generate so that I can focus on specific architectural aspects.

**Acceptance Criteria:**
- Dropdown selection for diagram types:
  - **Class Diagram**: Classes, attributes, methods, relationships
  - **Sequence Diagram**: Actor interactions and message flows
  - **Use Case Diagram**: Actors and use cases
  - **Activity Diagram**: Workflow and control flow
  - **Component Diagram**: Modules and interfaces
  - **Deployment Diagram**: Physical nodes and artifacts
  - **State Diagram**: Object states and transitions
- Brief description of each diagram type
- Default to Class Diagram

### US5: Diagram Generation
**As a user**, I want to generate UML diagrams from my selected directory so that I can visualize my code architecture.

**Acceptance Criteria:**
- "Generate Diagram" button that triggers API call
- Loading indicator during generation process
- Progress feedback for long-running operations
- Error handling with clear error messages
- Success confirmation with generation metadata

### US6: Diagram Viewing and Rendering
**As a user**, I want to view the generated diagrams in their native format so that I can immediately see the results.

**Acceptance Criteria:**
- **Mermaid Viewer**: Integrated Mermaid.js renderer for live preview
- **PlantUML Viewer**: Integration with PlantUML server or client-side renderer
- **DrawIO Viewer**: Embedded Draw.io viewer or XML display with download option
- Zoom, pan, and export capabilities for each viewer
- Raw code view option for all formats
- Copy to clipboard functionality

### US7: Results Management
**As a user**, I want to save, export, and manage my generated diagrams so that I can use them in documentation and presentations.

**Acceptance Criteria:**
- Download diagram as image (PNG, SVG)
- Download raw diagram code (XML, PlantUML, Mermaid)
- Save diagram to local file system
- Copy diagram code to clipboard
- Generation history/session management

## Technical Requirements

### Frontend Technology Stack
- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite for fast development and building
- **Styling**: Tailwind CSS for responsive design
- **State Management**: React Context or Zustand for simple state management
- **File System Access**: File System Access API (with fallback for unsupported browsers)

### Diagram Rendering Libraries
- **Mermaid**: `mermaid` npm package for Mermaid diagram rendering
- **PlantUML**: PlantUML server integration or `plantuml-encoder` for client-side rendering
- **DrawIO**: Embedded Draw.io viewer or custom XML parser

### API Integration
- **Backend URL**: Configurable endpoint (default: local Lambda or deployed AWS)
- **Request Format**: JSON POST to `/generate-diagram` endpoint
- **Response Handling**: Proper error handling and loading states
- **CORS**: Proper CORS configuration for local development

### File System Integration
- **Directory Access**: File System Access API for modern browsers
- **File Reading**: Recursive directory scanning with file content reading
- **File Filtering**: Support for multiple source code file extensions
- **Security**: Proper file access permissions and user consent

## API Integration Specification

### Request Format
```json
{
  "local_directory": "/path/to/source/code",
  "diagram_type": "class|sequence|use_case|activity|component|deployment|state",
  "output_format": "drawio|plantuml|mermaid",
  "analysis_method": "llm_direct|tree_sitter",
  "filters": {}
}
```

### Response Format
```json
{
  "diagram_code": "Generated diagram code in requested format",
  "format": "drawio|plantuml|mermaid",
  "metadata": {
    "source": {"type": "local_directory", "path": "..."},
    "files_analyzed": 15,
    "analysis_method": "llm_direct",
    "llm_provider": "GeminiProvider"
  },
  "success": true,
  "error": null
}
```

## User Interface Design

### Layout Structure
```
┌─────────────────────────────────────────────────────────┐
│                    Header / Title                        │
├─────────────────────────────────────────────────────────┤
│  Configuration Panel                                     │
│  ┌─────────────────┐ ┌─────────────────┐               │
│  │ Directory       │ │ Analysis Method │               │
│  │ Selector        │ │ Selection       │               │
│  └─────────────────┘ └─────────────────┘               │
│  ┌─────────────────┐ ┌─────────────────┐               │
│  │ Output Format   │ │ Diagram Type    │               │
│  │ Selection       │ │ Selection       │               │
│  └─────────────────┘ └─────────────────┘               │
│  ┌─────────────────────────────────────────────────────┐ │
│  │           Generate Diagram Button                   │ │
│  └─────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│                    Results Panel                         │
│  ┌─────────────────────────────────────────────────────┐ │
│  │                Diagram Viewer                       │ │
│  │            (Mermaid/PlantUML/DrawIO)               │ │
│  └─────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────┐ │
│  │              Export Options                         │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Component Hierarchy
```
App
├── Header
├── ConfigurationPanel
│   ├── DirectorySelector
│   ├── AnalysisMethodSelector
│   ├── OutputFormatSelector
│   ├── DiagramTypeSelector
│   └── GenerateButton
├── ResultsPanel
│   ├── DiagramViewer
│   │   ├── MermaidRenderer
│   │   ├── PlantUMLRenderer
│   │   └── DrawIORenderer
│   ├── CodeViewer
│   └── ExportOptions
└── LoadingOverlay
```

## Implementation Phases

### Phase 1: Basic UI Setup (1-2 days)
- Set up React + TypeScript + Vite project
- Create basic component structure
- Implement configuration panel UI
- Add Tailwind CSS styling

### Phase 2: File System Integration (2-3 days)
- Implement File System Access API
- Create directory selector component
- Add file filtering and reading logic
- Handle browser compatibility and fallbacks

### Phase 3: API Integration (1-2 days)
- Create API service layer
- Implement request/response handling
- Add loading states and error handling
- Test with backend API

### Phase 4: Diagram Rendering (3-4 days)
- Integrate Mermaid.js renderer
- Implement PlantUML rendering (server or client-side)
- Add DrawIO viewer integration
- Create unified viewer interface

### Phase 5: Export and Polish (1-2 days)
- Implement export functionality
- Add copy to clipboard features
- Polish UI/UX and responsive design
- Add comprehensive error handling

## Success Criteria
- Users can select local directories and generate UML diagrams
- All three output formats (DrawIO, PlantUML, Mermaid) render correctly
- Both analysis methods (AI and Tree-sitter) work properly
- Diagrams can be exported in multiple formats
- Interface is responsive and user-friendly
- Proper error handling and loading states
- Cross-browser compatibility (modern browsers)

## Future Enhancements
- GitHub repository integration (from existing backend)
- Diagram editing capabilities
- Multiple diagram comparison
- Batch processing for multiple directories
- Diagram templates and customization
- Integration with popular IDEs and editors