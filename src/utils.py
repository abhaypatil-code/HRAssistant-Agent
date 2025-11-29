"""
Utility functions for HR Copilot AI Agent
"""
from datetime import datetime
import streamlit as st


def format_date(date_str):
    """
    Format date string to readable format
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        
    Returns:
        Formatted date string
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%B %d, %Y")
    except:
        return date_str


def calculate_tenure(joining_date):
    """
    Calculate tenure from joining date
    
    Args:
        joining_date: Date string in YYYY-MM-DD format
        
    Returns:
        Tenure string (e.g., "3 years 2 months")
    """
    try:
        join_date = datetime.strptime(joining_date, "%Y-%m-%d")
        today = datetime.now()
        
        years = today.year - join_date.year
        months = today.month - join_date.month
        
        if months < 0:
            years -= 1
            months += 12
            
        if years > 0 and months > 0:
            return f"{years} year{'s' if years > 1 else ''} {months} month{'s' if months > 1 else ''}"
        elif years > 0:
            return f"{years} year{'s' if years > 1 else ''}"
        else:
            return f"{months} month{'s' if months > 1 else ''}"
    except:
        return "Unknown"


def format_leave_info(leave_type, balance):
    """
    Format leave information for display
    
    Args:
        leave_type: Type of leave
        balance: Leave balance
        
    Returns:
        Formatted string
    """
    return f"**{leave_type}**: {balance} day{'s' if balance != 1 else ''} remaining"


def init_session_state():
    """
    Initialize Streamlit session state variables
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "employee_id" not in st.session_state:
        st.session_state.employee_id = None
    
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    
    if "documents_loaded" not in st.session_state:
        st.session_state.documents_loaded = False


def add_message(role, content):
    """
    Add message to chat history
    
    Args:
        role: 'user' or 'assistant'
        content: Message content
    """
    st.session_state.messages.append({"role": role, "content": content})


def clear_chat_history():
    """
    Clear chat history
    """
    st.session_state.messages = []


def format_citation(source, page=None):
    """
    Format citation for RAG responses
    
    Args:
        source: Source document name
        page: Page number (optional)
        
    Returns:
        Formatted citation string
    """
    if page:
        return f"*[Source: {source}, Page {page}]*"
    return f"*[Source: {source}]*"


def extract_filename(filepath):
    """
    Extract filename from filepath
    
    Args:
        filepath: Full file path
        
    Returns:
        Filename without extension
    """
    import os
    filename = os.path.basename(filepath)
    return os.path.splitext(filename)[0].replace("_", " ").title()


def format_employee_info(emp_data):
    """
    Format employee information for display
    
    Args:
        emp_data: Dictionary containing employee data
        
    Returns:
        Formatted string
    """
    info = f"""
**Employee Information:**
- **Name**: {emp_data.get('Name', 'N/A')}
- **Employee ID**: {emp_data.get('EmpID', 'N/A')}
- **Department**: {emp_data.get('Department', 'N/A')}
- **Role**: {emp_data.get('Role', 'N/A')}
- **Manager**: {emp_data.get('Manager', 'N/A')}
- **Joining Date**: {format_date(emp_data.get('JoiningDate', 'N/A'))}
- **Tenure**: {calculate_tenure(emp_data.get('JoiningDate', 'N/A'))}

**Leave Balance:**
- **Casual Leave**: {emp_data.get('CasualLeave', 0)} days
- **Sick Leave**: {emp_data.get('SickLeave', 0)} days
- **Earned Leave**: {emp_data.get('EarnedLeave', 0)} days
"""
    return info.strip()


def is_valid_employee_id(emp_id):
    """
    Validate employee ID format
    
    Args:
        emp_id: Employee ID string
        
    Returns:
        Boolean indicating validity
    """
    if not emp_id:
        return False
    return emp_id.startswith('E') and len(emp_id) >= 4


def sanitize_query(query):
    """
    Sanitize user query
    
    Args:
        query: User query string
        
    Returns:
        Sanitized query
    """
    return query.strip()
