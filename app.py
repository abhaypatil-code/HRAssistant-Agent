"""
HR Copilot AI Agent - Streamlit Application
Main application file with chat interface
"""
import streamlit as st
import os
from src.employee_lookup import get_employee_lookup
from src.rag_pipeline import RAGPipeline, get_embeddings_model
from src.llm_orchestrator import LLMOrchestrator
from src.utils import init_session_state, add_message, clear_chat_history
import config


# Page configuration
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .sidebar-info {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_cached_embeddings():
    """
    Get cached embeddings model
    """
    return get_embeddings_model()


def initialize_app():
    """
    Initialize application components
    """
    init_session_state()
    
    # Initialize components (singleton pattern ensures single instance)
    if 'components_initialized' not in st.session_state:
        try:
            # Get cached embeddings
            embeddings = get_cached_embeddings()
            
            # Create new RAG pipeline for this session
            st.session_state.rag_pipeline = RAGPipeline(embeddings)
            
            # Get employee lookup (can be shared)
            st.session_state.employee_lookup = get_employee_lookup()
            
            # Create orchestrator with session-specific RAG pipeline
            st.session_state.orchestrator = LLMOrchestrator(
                rag_pipeline=st.session_state.rag_pipeline,
                employee_lookup=st.session_state.employee_lookup
            )
            
            st.session_state.components_initialized = True
        except Exception as e:
            st.error(f"Error initializing components: {e}")
            st.info("Please make sure you have set up your .env file with GOOGLE_API_KEY")
            st.stop()


def load_default_policies():
    """
    Load default policy documents from policies directory
    """
    if not st.session_state.documents_loaded:
        try:
            with st.spinner("Loading HR policy documents..."):
                rag_pipeline = st.session_state.rag_pipeline
                
                # Load documents from policies directory
                documents = rag_pipeline.load_documents_from_directory(config.POLICIES_DIR)
                
                if documents:
                    # Create vector store
                    rag_pipeline.create_vector_store(documents)
                    st.session_state.documents_loaded = True
                    st.sidebar.success(f"✓ Loaded {len(documents)} policy documents")
                else:
                    st.sidebar.warning("No policy documents found in policies directory")
        except Exception as e:
            st.sidebar.error(f"Error loading policies: {e}")


def render_sidebar():
    """
    Render sidebar with employee selection and file upload
    """
    st.sidebar.markdown("## 👤 Employee Selection")
    
    # Get employee IDs
    employee_lookup = st.session_state.employee_lookup
    employee_ids = employee_lookup.get_all_employee_ids()
    
    if not employee_ids:
        st.sidebar.error("No employee data found!")
        return
    
    # Employee ID selector
    selected_emp_id = st.sidebar.selectbox(
        "Select Your Employee ID",
        options=[""] + employee_ids,
        index=0,
        help="Select your employee ID to get personalized assistance"
    )
    
    # Update session state
    if selected_emp_id != st.session_state.employee_id:
        st.session_state.employee_id = selected_emp_id if selected_emp_id else None
        # Clear chat when employee changes
        clear_chat_history()
    
    # Display employee info if selected
    if st.session_state.employee_id:
        emp_info = employee_lookup.get_employee_info(st.session_state.employee_id)
        if emp_info:
            st.sidebar.markdown("### 📋 Your Information")
            st.sidebar.markdown(f"""
            <div class="sidebar-info">
            <b>Name:</b> {emp_info['Name']}<br>
            <b>Department:</b> {emp_info['Department']}<br>
            <b>Role:</b> {emp_info['Role']}<br>
            <b>Manager:</b> {emp_info['Manager']}
            </div>
            """, unsafe_allow_html=True)
            
            # Leave balance
            leave_info = employee_lookup.get_leave_balance(st.session_state.employee_id)
            if leave_info:
                st.sidebar.markdown("### 📅 Leave Balance")
                col1, col2, col3 = st.sidebar.columns(3)
                with col1:
                    st.metric("Casual", leave_info['CasualLeave'])
                with col2:
                    st.metric("Sick", leave_info['SickLeave'])
                with col3:
                    st.metric("Earned", leave_info['EarnedLeave'])
    
    st.sidebar.markdown("---")
    
    # Document upload section
    st.sidebar.markdown("## 📄 Upload Policy Documents")
    
    uploaded_files = st.sidebar.file_uploader(
        "Upload HR Policy PDFs",
        type=['pdf', 'txt'],
        accept_multiple_files=True,
        help="Upload additional HR policy documents"
    )
    
    if uploaded_files:
        if st.sidebar.button("Process Uploaded Documents"):
            with st.spinner("Processing documents..."):
                try:
                    rag_pipeline = st.session_state.rag_pipeline
                    
                    for uploaded_file in uploaded_files:
                        documents = rag_pipeline.process_uploaded_file(uploaded_file)
                        if documents:
                            if rag_pipeline.vector_store is None:
                                rag_pipeline.create_vector_store(documents)
                            else:
                                rag_pipeline.add_documents(documents)
                    
                    st.session_state.documents_loaded = True
                    st.sidebar.success(f"✓ Processed {len(uploaded_files)} document(s)")
                except Exception as e:
                    st.sidebar.error(f"Error processing documents: {e}")
    
    # Load default policies button
    if not st.session_state.documents_loaded:
        if st.sidebar.button("📚 Load Default Policies"):
            load_default_policies()
    else:
        st.sidebar.success("✓ Policy documents loaded")
    
    st.sidebar.markdown("---")
    
    # Clear chat button
    if st.sidebar.button("🗑️ Clear Chat History"):
        clear_chat_history()
        st.rerun()
    
    # Info section
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.info(
        "HR Copilot uses AI to answer your HR policy questions and "
        "provide personalized employee information. Ask me anything about "
        "leave policies, benefits, onboarding, or your personal HR data!"
    )


def render_chat_interface():
    """
    Render main chat interface
    """
    # Header
    st.markdown('<div class="main-header">👔 HR Copilot AI Agent</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Your intelligent HR assistant for policies and employee information</div>',
        unsafe_allow_html=True
    )
    
    # Display greeting if no messages
    if len(st.session_state.messages) == 0:
        orchestrator = st.session_state.orchestrator
        greeting = orchestrator.get_greeting(st.session_state.employee_id)
        
        with st.chat_message("assistant"):
            st.markdown(greeting)
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about HR policies or your employee information..."):
        # Add user message
        add_message("user", prompt)
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    orchestrator = st.session_state.orchestrator
                    
                    # Check if documents are loaded for policy questions
                    classification = orchestrator.classify_query(prompt)
                    if classification['needs_policy_data'] and not st.session_state.documents_loaded:
                        response_text = (
                            "I notice you're asking about HR policies, but no policy documents "
                            "have been loaded yet. Please click the '📚 Load Default Policies' "
                            "button in the sidebar to load the company's HR policy documents."
                        )
                    else:
                        # Generate response
                        response = orchestrator.generate_response(
                            query=prompt,
                            emp_id=st.session_state.employee_id,
                            conversation_history=st.session_state.messages
                        )
                        response_text = response['answer']
                    
                    st.markdown(response_text)
                    add_message("assistant", response_text)
                
                except Exception as e:
                    error_msg = f"I apologize, but I encountered an error: {str(e)}"
                    st.error(error_msg)
                    add_message("assistant", error_msg)


def main():
    """
    Main application entry point
    """
    # Initialize app
    initialize_app()
    
    # Render sidebar
    render_sidebar()
    
    # Render chat interface
    render_chat_interface()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
        "HR Copilot AI Agent | Powered by Google Gemini & LangChain"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
