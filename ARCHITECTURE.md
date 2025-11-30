# HR Assistant Agent - Architecture

This document outlines the end-to-end architecture of the HR Assistant Agent.

## Architecture Diagram

```mermaid
graph TD
    %% Nodes
    User([User])
    
    subgraph "Frontend (Streamlit)"
        UI[Streamlit App\n(app.py)]
    end

    subgraph "Orchestration Layer"
        Orchestrator[LLM Orchestrator\n(llm_orchestrator.py)]
        Router{Query Classifier}
        PromptBuilder[Prompt Builder]
    end

    subgraph "Data Layer"
        subgraph "RAG Pipeline (Policies)"
            Docs[Policy Documents\n(PDF/TXT)]
            Splitter[Text Splitter]
            EmbedModel[HuggingFace Embeddings\n(all-MiniLM-L6-v2)]
            VectorDB[(FAISS Vector Store)]
        end

        subgraph "Employee Data Engine"
            CSV[(Employee CSV)]
            Lookup[Employee Lookup Service\n(employee_lookup.py)]
        end
    end

    subgraph "AI Model Layer"
        Gemini[Google Gemini LLM]
    end

    %% Flows
    User <--> UI
    UI <--> Orchestrator
    Orchestrator --> Router
    
    %% Routing
    Router -- "Policy Query" --> VectorDB
    Router -- "Employee Query" --> Lookup
    Router -- "Hybrid" --> VectorDB & Lookup

    %% Data Retrieval
    Docs --> Splitter --> EmbedModel --> VectorDB
    VectorDB -- "Relevant Chunks" --> PromptBuilder
    CSV --> Lookup -- "Employee Context" --> PromptBuilder

    %% Generation
    PromptBuilder -- "Context + Query" --> Gemini
    Gemini -- "Response" --> Orchestrator
```

## Component Overview

### 1. Frontend (Streamlit)
- **File**: `app.py`
- **Role**: Handles user interaction, chat interface, file uploads, and session state management.
- **Key Features**: Dark mode UI, sidebar for settings, chat history display.

### 2. Orchestration Layer
- **File**: `src/llm_orchestrator.py`
- **Role**: The "brain" of the application.
- **Query Classifier**: Analyzes user input to determine if it requires Policy data, Employee data, or both.
- **Prompt Builder**: Combines the user query with retrieved context (policy chunks or employee info) to create a comprehensive prompt for the LLM.

### 3. Data Layer
#### RAG Pipeline (Policies)
- **File**: `src/rag_pipeline.py`
- **Role**: Handles unstructured data (PDFs/Text files).
- **Process**:
    1.  **Ingestion**: Loads documents.
    2.  **Splitting**: Breaks text into manageable chunks.
    3.  **Embedding**: Converts text to vectors using `sentence-transformers/all-MiniLM-L6-v2`.
    4.  **Storage**: Saves vectors in a local FAISS index.
    5.  **Retrieval**: Finds the most relevant chunks based on query similarity.

#### Employee Data Engine
- **File**: `src/employee_lookup.py`
- **Role**: Handles structured data (Employee CSV).
- **Process**: Loads employee records into a Pandas DataFrame and provides methods to look up specific details (Leave Balance, Manager, Department).

### 4. AI Model Layer
- **Service**: Google Gemini API
- **Role**: Generates the final natural language response based on the prompt constructed by the Orchestrator.
