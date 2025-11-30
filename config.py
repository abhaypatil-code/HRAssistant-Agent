"""
Configuration settings for HR Copilot AI Agent

This module centralizes all configuration parameters for the HR Assistant Agent.
It loads environment variables from .env and provides default values for all settings.

Configuration Categories:
- API Configuration: Google Gemini API settings
- Model Settings: LLM behavior parameters
- RAG Settings: Retrieval Augmented Generation parameters
- File Paths: Data and storage locations
- UI Settings: Streamlit application settings
- Query Classification: Keyword lists for routing queries

Usage:
    import config
    api_key = config.GOOGLE_API_KEY
    model = config.MODEL_NAME

Note:
    All environment variables are optional except GOOGLE_API_KEY.
    Default values are provided for all other settings.
"""
import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
# This must be called before accessing os.getenv()
load_dotenv()

# ============================================================================
# API Configuration
# ============================================================================

# Google Gemini API key - REQUIRED
# Get your API key at: https://aistudio.google.com/app/apikey
# This is the only required environment variable for the application to run
# Priority: Streamlit secrets > Environment variable
if "GOOGLE_API_KEY" in st.secrets:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Validate that API key is set
if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found. "
        "Please set it in .streamlit/secrets.toml or as an environment variable."
    )

# ============================================================================
# Model Settings
# ============================================================================

# Gemini model to use for response generation
# Options:
#   - gemini-2.0-flash: Latest, fast, cost-effective (recommended)
#   - gemini-pro: Higher quality, slower, more expensive
#   - gemini-1.5-flash: Previous generation
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.0-flash")

# Temperature controls randomness in responses (0.0 to 1.0)
# Lower values (0.0-0.3): More deterministic, factual responses
# Medium values (0.4-0.7): Balanced creativity and consistency
# Higher values (0.8-1.0): More creative, varied responses
# Default: 0.7 for natural, friendly HR responses
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# Maximum number of tokens in generated responses
# Higher values allow longer responses but increase cost and latency
# Typical range: 512-2048
# Default: 1024 (sufficient for most HR queries)
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))

# ============================================================================
# RAG (Retrieval Augmented Generation) Settings
# ============================================================================

# Number of characters per document chunk
# Smaller chunks: More precise retrieval but may lose context
# Larger chunks: More context but less precise
# Recommended range: 500-1500
# Default: 1000 works well for HR policy documents
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))

# Number of overlapping characters between consecutive chunks
# Overlap helps maintain context across chunk boundaries
# Typically 10-20% of CHUNK_SIZE
# Default: 200 (20% of default chunk size)
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# Number of document chunks to retrieve for each query (Top-K)
# More chunks: More context but slower and more tokens used
# Fewer chunks: Faster but may miss relevant information
# Recommended range: 3-6
# Default: 4 provides good balance of relevance and performance
RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", "4"))

# Minimum similarity score for retrieved chunks (0.0 to 1.0)
# Higher values: Only highly relevant chunks are retrieved
# Lower values: More permissive retrieval
# Default: 0.5 for balanced relevance
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.5"))

# ============================================================================
# File Paths
# ============================================================================

# Base data directory
# All data files are stored relative to this directory
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# Employee data CSV file path
# Contains employee information: ID, name, department, leave balances, etc.
# Default: data/employee_data.csv
EMPLOYEE_DATA_PATH = os.getenv(
    "EMPLOYEE_DATA_PATH",
    os.path.join(DATA_DIR, "employee_data.csv")
)

# HR policy documents directory
# Contains policy documents in PDF or TXT format
# Default: data/policies/
POLICIES_DIR = os.getenv(
    "POLICIES_DIR",
    os.path.join(DATA_DIR, "policies")
)

# Vector store persistence path
# FAISS vector store is saved here for faster subsequent loads
# Default: data/vector_store/
VECTOR_STORE_PATH = os.getenv(
    "VECTOR_STORE_PATH",
    os.path.join(DATA_DIR, "vector_store")
)

# ============================================================================
# Streamlit UI Settings
# ============================================================================

# Page title displayed in browser tab
PAGE_TITLE = os.getenv("PAGE_TITLE", "HR Copilot AI Agent")

# Page icon displayed in browser tab (emoji or image path)
PAGE_ICON = os.getenv("PAGE_ICON", "👔")

# ============================================================================
# Query Classification Keywords
# ============================================================================
# These keywords are used to classify user queries and route them to the
# appropriate data source (employee data vs. policy documents)

# Keywords indicating employee-specific queries
# Queries containing these words typically need employee data
# Examples: "my leave balance", "who is my manager"
EMPLOYEE_KEYWORDS = [
    "my", "i", "me", "balance", "manager", "leaves left",
    "my department", "my role", "my manager", "how many leaves",
    "contact", "who is", "when did i join", "my email", "my phone"
]

# Keywords indicating policy-related queries
# Queries containing these words typically need policy documents
# Examples: "what is the maternity policy", "how to apply for leave"
POLICY_KEYWORDS = [
    "policy", "policies", "benefits", "maternity", "paternity",
    "onboarding", "handbook", "guide", "eligibility", "apply for",
    "procedure", "process", "rules", "regulations", "entitled",
    "sick leave policy", "casual leave", "earned leave", "how to"
]

# ============================================================================
# Advanced Settings (Typically not changed)
# ============================================================================

# Logging level for application logs
# Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Application environment (development, staging, production)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Debug mode for development
# Set to False in production for better performance
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# ============================================================================
# Validation
# ============================================================================

def validate_config():
    """
    Validate configuration settings and paths.
    
    Raises:
        FileNotFoundError: If required files or directories don't exist
        ValueError: If configuration values are invalid
    """
    # Validate temperature range
    if not 0.0 <= TEMPERATURE <= 1.0:
        raise ValueError(f"TEMPERATURE must be between 0.0 and 1.0, got {TEMPERATURE}")
    
    # Validate retrieval K
    if RETRIEVAL_K < 1:
        raise ValueError(f"RETRIEVAL_K must be at least 1, got {RETRIEVAL_K}")
    
    # Validate chunk settings
    if CHUNK_SIZE < 100:
        raise ValueError(f"CHUNK_SIZE too small: {CHUNK_SIZE}")
    if CHUNK_OVERLAP >= CHUNK_SIZE:
        raise ValueError(f"CHUNK_OVERLAP ({CHUNK_OVERLAP}) must be less than CHUNK_SIZE ({CHUNK_SIZE})")
    
    # Check if employee data exists
    if not os.path.exists(EMPLOYEE_DATA_PATH):
        print(f"Warning: Employee data file not found at {EMPLOYEE_DATA_PATH}")
    
    # Check if policies directory exists
    if not os.path.exists(POLICIES_DIR):
        print(f"Warning: Policies directory not found at {POLICIES_DIR}")
        print(f"Creating policies directory: {POLICIES_DIR}")
        os.makedirs(POLICIES_DIR, exist_ok=True)


# Run validation on import (optional, can comment out for production)
if DEBUG:
    validate_config()

