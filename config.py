"""
Configuration settings for HR Copilot AI Agent
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Model Settings
MODEL_NAME = "gemini-1.5-flash"
TEMPERATURE = 0.7
MAX_TOKENS = 1024

# RAG Settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVAL_K = 4  # Number of chunks to retrieve
SIMILARITY_THRESHOLD = 0.5

# File Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
EMPLOYEE_DATA_PATH = os.path.join(DATA_DIR, "employee_data.csv")
POLICIES_DIR = os.path.join(DATA_DIR, "policies")
VECTOR_STORE_PATH = os.path.join(DATA_DIR, "vector_store")

# Streamlit Settings
PAGE_TITLE = "HR Copilot AI Agent"
PAGE_ICON = "👔"

# Query Classification Keywords
EMPLOYEE_KEYWORDS = [
    "my", "i", "me", "balance", "manager", "leaves left", 
    "my department", "my role", "my manager", "how many leaves"
]

POLICY_KEYWORDS = [
    "policy", "policies", "benefits", "maternity", "paternity",
    "onboarding", "handbook", "guide", "eligibility", "apply for"
]
