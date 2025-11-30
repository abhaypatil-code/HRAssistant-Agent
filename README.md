# HR Copilot AI Agent 👔

An intelligent, production-ready HR assistant that combines **Retrieval Augmented Generation (RAG)** over HR policy documents with **structured employee data lookup** to answer both policy-related and employee-specific questions through a conversational Streamlit interface.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/) [![AI](https://img.shields.io/badge/AI-Google%20Gemini-4285F4)](https://ai.google.dev/) [![Framework](https://img.shields.io/badge/Framework-LangChain-green)](https://python.langchain.com/) [![UI](https://img.shields.io/badge/UI-Streamlit-FF4B4B)](https://streamlit.io/) [![Vector DB](https://img.shields.io/badge/VectorDB-FAISS-orange)](https://faiss.ai/) [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/HRAssistant-Agent.git
cd HRAssistant-Agent

# Set up environment (Windows)
setup.bat

# Or manually:
python -m venv venv
venv\Scripts\activate  # On Linux/Mac: source venv/bin/activate
pip install -r requirements.txt

# Configure API key
copy .env.example .env  # On Linux/Mac: cp .env.example .env
# Edit .env and add your Google Gemini API key

# Run the application
streamlit run app.py
```

**Get your free Gemini API key:** [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

---

## 📋 Overview

HR Copilot is an end-to-end AI-powered HR assistant that helps employees get instant answers to their HR-related questions. It intelligently combines:

- **RAG (Retrieval Augmented Generation)** for answering policy questions from HR documents
- **Structured data lookup** for employee-specific information (leave balance, manager info, etc.)
- **Smart query routing** to determine which data sources to use
- **Conversational interface** for natural, friendly interactions

### Example Queries

**Policy Questions:**
- "What is our maternity leave policy?"
- "What benefits do new employees get?"
- "How do I apply for leave?"

**Employee-Specific Questions:**
- "How many casual leaves do I have left?"
- "Who is my manager?"
- "What is my department?"

**Hybrid Questions:**
- "Can I take 5 days of sick leave based on my balance?"
- "Am I eligible for the benefits mentioned in the handbook?"

## ✨ Features

### Core Capabilities
- ✅ **RAG over HR Policy PDFs** - Semantic search over company policy documents
- ✅ **Employee Data Lookup** - Query employee information from CSV database
- ✅ **Smart Query Classification** - Automatically routes queries to appropriate data sources
- ✅ **Conversational Chat Interface** - Natural language interactions with chat history
- ✅ **Personalized Responses** - Context-aware answers based on employee ID
- ✅ **Source Citations** - Policy answers include document references
- ✅ **Document Upload** - Add new policy documents on the fly
- ✅ **Leave Balance Display** - Quick view of employee leave balances

### User Interface Features
- 📊 Employee ID selector with auto-populated dropdown
- 📄 PDF/TXT document uploader for HR policies
- 💬 Chat interface with conversation history
- 📋 Sidebar showing employee info and leave balance
- 🎨 Clean, professional UI with custom styling

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **AI Model** | Google Gemini (gemini-1.5-flash) | LLM for response generation |
| **Framework** | LangChain | RAG pipeline orchestration |
| **Vector DB** | FAISS | In-memory vector storage for embeddings |
| **Embeddings** | Google Generative AI Embeddings | Document and query embeddings |
| **UI** | Streamlit | Web application interface |
| **Data Processing** | Pandas | Employee data manipulation |
| **PDF Processing** | PyPDF | PDF document parsing |

## 📁 Project Structure

```
hr_copilot/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
├── data/
│   ├── employee_data.csv      # Employee database (15 sample employees)
│   └── policies/              # HR policy documents
│       ├── leave_policy.txt
│       ├── benefits_handbook.txt
│       └── onboarding_guide.txt
└── src/
    ├── __init__.py
    ├── employee_lookup.py     # Employee data query tool
    ├── rag_pipeline.py        # RAG implementation
    ├── llm_orchestrator.py    # Query routing & LLM logic
    └── utils.py               # Helper functions
```

# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```

2. Get your Google Gemini API key:
   - Visit: https://aistudio.google.com/app/apikey
   - Create a new API key (free tier available)

3. Edit `.env` file and add your API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

### Step 5: Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

> [!TIP]
> For detailed deployment instructions for production environments, see [DEPLOYMENT.md](DEPLOYMENT.md)

## 📖 Usage Guide

### First Time Setup

1. **Launch the app** - Run `streamlit run app.py`
2. **Load policies** - Click "📚 Load Default Policies" in the sidebar
3. **Select employee** - Choose an employee ID from the dropdown
4. **Start chatting** - Ask your HR questions!

### Using the Application

#### Employee Selection
- Select your Employee ID from the sidebar dropdown
- Your information and leave balance will be displayed
- Responses will be personalized based on your employee data

#### Asking Questions

**For Policy Questions:**
```
"What is our maternity leave policy?"
"How many days of earned leave can I carry forward?"
"What benefits do I get as a new employee?"
```

**For Personal HR Data:**
```
"How many casual leaves do I have left?"
"Who is my manager and how can I contact them?"
"What is my department and role?"
```

**For Combined Queries:**
```
"Based on my leave balance, can I take 10 days off?"
"Am I eligible for the gym membership benefit?"
```

#### Uploading New Documents

1. Click "Browse files" in the sidebar
2. Select PDF or TXT files containing HR policies
3. Click "Process Uploaded Documents"
4. The documents will be added to the knowledge base

#### Managing Chat

- **Clear History** - Click "🗑️ Clear Chat History" to start fresh
- **Change Employee** - Select a different employee ID to switch context

## 🏗️ Architecture

### System Flow

```
User Query → Query Classification → Data Retrieval → Response Generation
                    ↓
        ┌──────────┴──────────┐
        ↓                     ↓
   Employee Data          Policy RAG
   (CSV Lookup)         (Vector Search)
        ↓                     ↓
        └──────────┬──────────┘
                   ↓
            Context Merging
                   ↓
              LLM (Gemini)
                   ↓
         Formatted Response
```

### Components

#### 1. Employee Lookup (`employee_lookup.py`)
- Loads employee data from CSV
- Provides query methods for leave balance, manager info, department details
- Formats responses in friendly HR tone

#### 2. RAG Pipeline (`rag_pipeline.py`)
- Processes PDF/TXT documents
- Chunks documents using RecursiveCharacterTextSplitter
- Creates embeddings using Google Generative AI
- Stores in FAISS vector database
- Performs semantic search for relevant context

#### 3. LLM Orchestrator (`llm_orchestrator.py`)
- Classifies queries using keyword matching
- Routes to appropriate data sources
- Gathers context from employee data and/or policy documents
- Generates responses using Gemini
- Adds citations for policy-based answers

#### 4. Streamlit App (`app.py`)
- Renders chat interface
- Manages session state
- Handles employee selection
- Processes document uploads
- Displays employee information

## 📊 Sample Data

### Employee Data
The project includes 15 sample employees across different departments:
- Engineering (6 employees)
- HR (3 employees)
- Marketing (3 employees)
- Finance (3 employees)

Each employee has:
- Personal info (name, email, phone)
- Department and role
- Manager assignment
- Joining date
- Leave balances (Casual, Sick, Earned)

### Policy Documents
Three comprehensive policy documents are included:

1. **Leave Policy** - All leave types, eligibility, application process
2. **Benefits Handbook** - Health insurance, financial benefits, perks
3. **Onboarding Guide** - First day, first week, 90-day plan

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Model Settings
MODEL_NAME = "gemini-1.5-flash"  # Change to gemini-pro for better quality
TEMPERATURE = 0.7                 # Lower for more deterministic responses
MAX_TOKENS = 1024                 # Increase for longer responses

# RAG Settings
CHUNK_SIZE = 1000                 # Size of document chunks
CHUNK_OVERLAP = 200               # Overlap between chunks
RETRIEVAL_K = 4                   # Number of chunks to retrieve

# Query Classification Keywords
EMPLOYEE_KEYWORDS = [...]         # Keywords for employee queries
POLICY_KEYWORDS = [...]           # Keywords for policy queries
```

## 🔧 Troubleshooting

### Common Issues

**Issue: "GOOGLE_API_KEY not found"**
- Solution: Make sure you've created a `.env` file with your API key
- Check that the `.env` file is in the `hr_copilot` directory

**Issue: "No employee data found"**
- Solution: Verify `data/employee_data.csv` exists
- Check file path in `config.py`

**Issue: "No policy documents found"**
- Solution: Click "📚 Load Default Policies" button
- Verify files exist in `data/policies/` directory

**Issue: "Error initializing embeddings"**
- Solution: Check your API key is valid
- Ensure you have internet connection
- Verify API key has not exceeded quota

**Issue: Slow response times**
- Solution: Reduce `RETRIEVAL_K` in config.py
- Use smaller documents
- Consider upgrading to Gemini Pro for better performance

## 🚀 Potential Improvements

### Short-term Enhancements
- [ ] Add Google Sheets integration for live employee data
- [ ] Implement user authentication
- [ ] Add conversation export functionality
- [ ] Support for more document formats (DOCX, HTML)
- [ ] Multi-language support

### Medium-term Features
- [ ] Integration with calendar APIs (Google Calendar, Outlook)
- [ ] Leave application workflow automation
- [ ] Email notifications for HR queries
- [ ] Analytics dashboard for HR team
- [ ] Mobile-responsive design

### Advanced Features
- [ ] Voice input/output support
- [ ] Integration with HRIS systems (Workday, BambooHR)
- [ ] Automated policy update detection
- [ ] Advanced analytics (query trends, common questions)
- [ ] Role-based access control
- [ ] Multi-tenant support for different companies

### Technical Improvements
- [ ] Add caching for faster responses
- [ ] Implement async processing for large documents
- [ ] Add comprehensive unit tests
- [ ] Set up CI/CD pipeline
- [ ] Docker containerization
- [ ] Database migration (PostgreSQL/MongoDB)
- [ ] API endpoint creation (FastAPI)

## 📝 Limitations

### Current Limitations
1. **Data Storage**: Uses CSV files (not suitable for production scale)
2. **Authentication**: No user authentication (anyone can select any employee ID)
3. **Real-time Updates**: Employee data is static (no live sync)
4. **Document Processing**: Limited to PDF and TXT formats
5. **Scalability**: In-memory FAISS (not suitable for very large document sets)
6. **Query Routing**: Simple keyword-based (could be improved with ML)
7. **API Costs**: Gemini API has rate limits and quotas

### Known Issues
- Large PDFs may take time to process
- Very long conversations may exceed context window
- No conversation persistence (cleared on page refresh)

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**For production deployment:**
- See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment guides (Streamlit Cloud, AWS, GCP, Azure, Heroku)
- Review [docs/architecture.md](docs/architecture.md) for system architecture
- Implement authentication and authorization for security
- Use production database (PostgreSQL, MongoDB) instead of CSV
- Set up monitoring, logging, and alerting
- Implement rate limiting and caching
- Add comprehensive testing coverage

## 📚 Documentation

- **[README.md](README.md)** - This file, getting started guide
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete project overview and repository summary
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines and development setup
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide for various platforms
- **[docs/architecture.md](docs/architecture.md)** - Detailed system architecture and design
- **[QUICKSTART.md](QUICKSTART.md)** - Quick reference guide
- **[PROJECT_COMPLETE.md](PROJECT_COMPLETE.md)** - Project completion summary

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Support

- **Issues**: Open an issue on GitHub for bug reports or feature requests
- **Discussions**: Use GitHub Discussions for questions and community support
- **Documentation**: Check the documentation files listed above

## 🙏 Acknowledgments

- **Google Gemini** for the powerful LLM capabilities
- **LangChain** for RAG orchestration framework
- **Streamlit** for the intuitive web framework
- **FAISS** for efficient vector similarity search
- **HuggingFace** for embedding models

---

**Built with ❤️ using Google Gemini, LangChain, and Streamlit**

**Production Ready** | **Fully Documented** | **Easy to Deploy**

Last Updated: November 2024
