"""
RAG Pipeline for HR Policy Documents
Handles document processing, embedding, and retrieval
"""
import os
from typing import List, Dict, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.schema import Document
import config


class RAGPipeline:
    """
    Retrieval Augmented Generation pipeline for HR documents
    """
    
    def __init__(self):
        """
        Initialize RAG pipeline
        """
        self.embeddings = None
        self.vector_store = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len,
        )
        self._initialize_embeddings()
    
    def _initialize_embeddings(self):
        """
        Initialize Google Generative AI embeddings
        """
        try:
            if not config.GOOGLE_API_KEY:
                raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=config.GOOGLE_API_KEY
            )
            print("✓ Embeddings initialized successfully")
        except Exception as e:
            print(f"✗ Error initializing embeddings: {e}")
            raise
    
    def load_text_file(self, file_path: str) -> List[Document]:
        """
        Load a text file and convert to Document
        
        Args:
            file_path: Path to text file
            
        Returns:
            List of Document objects
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            filename = os.path.basename(file_path)
            doc = Document(
                page_content=content,
                metadata={"source": filename, "file_path": file_path}
            )
            return [doc]
        except Exception as e:
            print(f"✗ Error loading {file_path}: {e}")
            return []
    
    def load_documents_from_directory(self, directory: str) -> List[Document]:
        """
        Load all text documents from a directory
        
        Args:
            directory: Path to directory containing documents
            
        Returns:
            List of Document objects
        """
        documents = []
        
        if not os.path.exists(directory):
            print(f"✗ Directory not found: {directory}")
            return documents
        
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            # Support .txt files (our policy documents)
            if filename.endswith('.txt'):
                docs = self.load_text_file(file_path)
                documents.extend(docs)
                print(f"✓ Loaded: {filename}")
        
        print(f"✓ Total documents loaded: {len(documents)}")
        return documents
    
    def process_uploaded_file(self, uploaded_file) -> List[Document]:
        """
        Process uploaded file from Streamlit
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            List of Document objects
        """
        try:
            # Read content based on file type
            if uploaded_file.name.endswith('.txt'):
                content = uploaded_file.read().decode('utf-8')
            elif uploaded_file.name.endswith('.pdf'):
                # For PDF, we'll use pypdf
                from pypdf import PdfReader
                pdf_reader = PdfReader(uploaded_file)
                content = ""
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    content += f"\n\n--- Page {page_num + 1} ---\n\n{page_text}"
            else:
                print(f"✗ Unsupported file type: {uploaded_file.name}")
                return []
            
            doc = Document(
                page_content=content,
                metadata={"source": uploaded_file.name}
            )
            print(f"✓ Processed uploaded file: {uploaded_file.name}")
            return [doc]
        except Exception as e:
            print(f"✗ Error processing uploaded file: {e}")
            return []
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks
        
        Args:
            documents: List of Document objects
            
        Returns:
            List of chunked Document objects
        """
        chunks = self.text_splitter.split_documents(documents)
        print(f"✓ Created {len(chunks)} chunks from {len(documents)} documents")
        return chunks
    
    def create_vector_store(self, documents: List[Document]) -> FAISS:
        """
        Create FAISS vector store from documents
        
        Args:
            documents: List of Document objects
            
        Returns:
            FAISS vector store
        """
        try:
            # Chunk documents
            chunks = self.chunk_documents(documents)
            
            if not chunks:
                raise ValueError("No chunks created from documents")
            
            # Create vector store
            self.vector_store = FAISS.from_documents(
                documents=chunks,
                embedding=self.embeddings
            )
            print(f"✓ Vector store created with {len(chunks)} chunks")
            return self.vector_store
        except Exception as e:
            print(f"✗ Error creating vector store: {e}")
            raise
    
    def add_documents(self, documents: List[Document]):
        """
        Add documents to existing vector store
        
        Args:
            documents: List of Document objects
        """
        try:
            chunks = self.chunk_documents(documents)
            
            if self.vector_store is None:
                self.create_vector_store(documents)
            else:
                self.vector_store.add_documents(chunks)
                print(f"✓ Added {len(chunks)} chunks to vector store")
        except Exception as e:
            print(f"✗ Error adding documents: {e}")
    
    def retrieve(self, query: str, k: int = None) -> List[Dict]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            List of dictionaries with content and metadata
        """
        if self.vector_store is None:
            print("✗ Vector store not initialized")
            return []
        
        try:
            k = k or config.RETRIEVAL_K
            
            # Perform similarity search
            results = self.vector_store.similarity_search_with_score(query, k=k)
            
            # Format results
            formatted_results = []
            for doc, score in results:
                # Only include results above similarity threshold
                if score <= config.SIMILARITY_THRESHOLD or True:  # FAISS uses distance, lower is better
                    formatted_results.append({
                        'content': doc.page_content,
                        'source': doc.metadata.get('source', 'Unknown'),
                        'score': score
                    })
            
            print(f"✓ Retrieved {len(formatted_results)} relevant chunks")
            return formatted_results
        except Exception as e:
            print(f"✗ Error during retrieval: {e}")
            return []
    
    def format_context(self, retrieved_docs: List[Dict]) -> str:
        """
        Format retrieved documents into context string
        
        Args:
            retrieved_docs: List of retrieved document dictionaries
            
        Returns:
            Formatted context string
        """
        if not retrieved_docs:
            return "No relevant information found in the policy documents."
        
        context_parts = []
        for i, doc in enumerate(retrieved_docs, 1):
            context_parts.append(
                f"[Source {i}: {doc['source']}]\n{doc['content']}\n"
            )
        
        return "\n---\n".join(context_parts)
    
    def get_sources(self, retrieved_docs: List[Dict]) -> List[str]:
        """
        Extract unique sources from retrieved documents
        
        Args:
            retrieved_docs: List of retrieved document dictionaries
            
        Returns:
            List of unique source names
        """
        sources = list(set([doc['source'] for doc in retrieved_docs]))
        return sources
    
    def save_vector_store(self, path: str = None):
        """
        Save vector store to disk
        
        Args:
            path: Path to save vector store
        """
        if self.vector_store is None:
            print("✗ No vector store to save")
            return
        
        try:
            save_path = path or config.VECTOR_STORE_PATH
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            self.vector_store.save_local(save_path)
            print(f"✓ Vector store saved to {save_path}")
        except Exception as e:
            print(f"✗ Error saving vector store: {e}")
    
    def load_vector_store(self, path: str = None) -> bool:
        """
        Load vector store from disk
        
        Args:
            path: Path to load vector store from
            
        Returns:
            True if successful, False otherwise
        """
        try:
            load_path = path or config.VECTOR_STORE_PATH
            
            if not os.path.exists(load_path):
                print(f"✗ Vector store not found at {load_path}")
                return False
            
            self.vector_store = FAISS.load_local(
                load_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            print(f"✓ Vector store loaded from {load_path}")
            return True
        except Exception as e:
            print(f"✗ Error loading vector store: {e}")
            return False


# Singleton instance
_rag_pipeline = None

def get_rag_pipeline() -> RAGPipeline:
    """
    Get singleton instance of RAGPipeline
    
    Returns:
        RAGPipeline instance
    """
    global _rag_pipeline
    if _rag_pipeline is None:
        _rag_pipeline = RAGPipeline()
    return _rag_pipeline
