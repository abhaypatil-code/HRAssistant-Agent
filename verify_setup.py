"""
HR Assistant Agent - Setup Verification Script
Verifies that all required components are properly installed and configured
"""

import sys
import os
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_status(check_name, status, message=""):
    """Print check status"""
    symbol = "✓" if status else "✗"
    status_text = "PASS" if status else "FAIL"
    color = "\033[92m" if status else "\033[91m"
    reset = "\033[0m"
    
    print(f"{color}{symbol} {check_name}: {status_text}{reset}")
    if message:
        print(f"  → {message}")

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    is_valid = version.major == 3 and version.minor >= 8
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print_status(
        "Python Version",
        is_valid,
        f"Python {version_str} {'(OK)' if is_valid else '(Requires 3.8+)'}"
    )
    return is_valid

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'langchain',
        'langchain_google_genai',
        'google.generativeai',
        'faiss',
        'pypdf',
        'pandas',
        'dotenv'
    ]
    
    all_installed = True
    missing = []
    
    for package in required_packages:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            elif package == 'faiss':
                __import__('faiss')
            else:
                __import__(package.replace('-', '_'))
        except ImportError:
            all_installed = False
            missing.append(package)
    
    message = "All packages installed" if all_installed else f"Missing: {', '.join(missing)}"
    print_status(
        "Required Packages",
        all_installed,
        message
    )
    return all_installed

def check_env_file():
    """Check if .env file exists and has API key"""
    env_path = Path('.env')
    
    if not env_path.exists():
        print_status(
            ".env File",
            False,
            "File not found. Required for local development (copy .env.example)"
        )
        return False
    
    # Check if API key is set
    with open(env_path, 'r') as f:
        content = f.read()
        has_key = 'GOOGLE_API_KEY=' in content and 'your_gemini_api_key_here' not in content
    
    print_status(
        ".env File",
        has_key,
        "API key configured" if has_key else "Please add your GOOGLE_API_KEY"
    )
    return has_key

def check_data_files():
    """Check if required data files exist"""
    required_files = [
        'data/employee_data.csv',
        'data/policies/leave_policy.txt',
        'data/policies/benefits_handbook.txt',
        'data/policies/onboarding_guide.txt'
    ]
    
    all_exist = True
    missing = []
    
    for file_path in required_files:
        if not Path(file_path).exists():
            all_exist = False
            missing.append(file_path)
    
    message = "All data files present" if all_exist else f"Missing: {', '.join(missing)}"
    print_status(
        "Data Files",
        all_exist,
        message
    )
    return all_exist

def check_source_files():
    """Check if source code files exist"""
    required_files = [
        'app.py',
        'config.py',
        'src/__init__.py',
        'src/employee_lookup.py',
        'src/rag_pipeline.py',
        'src/llm_orchestrator.py',
        'src/utils.py'
    ]
    
    all_exist = True
    missing = []
    
    for file_path in required_files:
        if not Path(file_path).exists():
            all_exist = False
            missing.append(file_path)
    
    message = "All source files present" if all_exist else f"Missing: {', '.join(missing)}"
    print_status(
        "Source Files",
        all_exist,
        message
    )
    return all_exist

def check_config():
    """Check if config can be loaded"""
    try:
        import config
        print_status(
            "Configuration",
            True,
            f"Model: {config.MODEL_NAME}, Temp: {config.TEMPERATURE}"
        )
        return True
    except Exception as e:
        print_status(
            "Configuration",
            False,
            f"Error: {str(e)}"
        )
        return False

def main():
    """Run all verification checks"""
    print_header("HR Assistant Agent - Setup Verification")
    
    checks = {
        "Python Version": check_python_version(),
        "Dependencies": check_dependencies(),
        "Environment File": check_env_file(),
        "Data Files": check_data_files(),
        "Source Files": check_source_files(),
        "Configuration": check_config()
    }
    
    print_header("Verification Summary")
    
    passed = sum(checks.values())
    total = len(checks)
    
    print(f"\nPassed: {passed}/{total} checks")
    
    if passed == total:
        print("\n✅ All checks passed! Your setup is complete.")
        print("\nNext steps:")
        print("  1. Run: streamlit run app.py")
        print("  2. Open browser at http://localhost:8501")
        print("  3. Click 'Load Default Policies' in sidebar")
        print("  4. Select an employee ID")
        print("  5. Start asking questions!")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Create .env file: copy .env.example .env")
        print("  - Add API key to .env file")
    
    print("\n" + "="*60 + "\n")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
