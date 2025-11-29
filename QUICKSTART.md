# Quick Start Guide - HR Copilot AI Agent

## 🚀 Get Started in 5 Minutes

### Step 1: Get Your API Key (2 minutes)

1. Visit: https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### Step 2: Setup (2 minutes)

**Option A: Automated Setup (Recommended for Windows)**
```bash
# Run the setup script
setup.bat
```

**Option B: Manual Setup**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env  # Windows
# OR
cp .env.example .env    # Linux/Mac

# Edit .env and add your API key
notepad .env  # Windows
# OR
nano .env     # Linux/Mac
```

Add your API key to `.env`:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

### Step 3: Run the Application (1 minute)

**Option A: Using Run Script (Windows)**
```bash
run.bat
```

**Option B: Manual Run**
```bash
# Make sure virtual environment is activated
streamlit run app.py
```

The app will open automatically at: http://localhost:8501

### Step 4: Start Using HR Copilot

1. **Load Policies**: Click "📚 Load Default Policies" in the sidebar
2. **Select Employee**: Choose an employee ID from the dropdown (try E001)
3. **Ask Questions**: Start chatting!

## 📝 Example Questions to Try

### Policy Questions
```
What is our maternity leave policy?
How many days of casual leave am I entitled to?
What benefits do new employees get?
How do I apply for leave?
What is the process for bereavement leave?
```

### Employee-Specific Questions
```
How many casual leaves do I have left?
Who is my manager?
What is my department?
Show me my leave balance
What is my role?
```

### Hybrid Questions
```
Can I take 5 days of sick leave based on my balance?
Am I eligible for the gym membership benefit?
How do I contact my manager about taking leave?
```

## 🎯 Tips for Best Results

1. **Be Specific**: Ask clear, specific questions
2. **Use Natural Language**: Talk to the bot like you would to an HR person
3. **Select Your Employee ID**: For personalized answers about leave balance, manager, etc.
4. **Load Policies First**: Click "Load Default Policies" before asking policy questions

## 🔧 Troubleshooting

### "GOOGLE_API_KEY not found"
- Make sure you created a `.env` file
- Check that your API key is correctly pasted
- Restart the application after adding the API key

### "No policy documents found"
- Click the "📚 Load Default Policies" button in the sidebar
- Wait for the success message before asking policy questions

### Application won't start
- Make sure you activated the virtual environment
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version: `python --version` (should be 3.8+)

### Slow responses
- First query may be slower (initializing models)
- Subsequent queries should be faster
- Check your internet connection

## 📊 Sample Employee IDs

Try these employee IDs to test different scenarios:

- **E001** - Rajesh Kumar (Engineering, Senior Software Engineer)
- **E002** - Priya Sharma (Engineering Manager)
- **E004** - Sneha Reddy (HR Manager)
- **E006** - Ananya Iyer (Marketing Specialist)
- **E009** - Meera Nair (Financial Analyst)

## 🎨 Features to Explore

- ✅ Chat with conversation history
- ✅ View employee info and leave balance in sidebar
- ✅ Upload additional policy documents
- ✅ Clear chat history
- ✅ Switch between different employees
- ✅ Get citations for policy answers

## 📚 Next Steps

Once you're comfortable with the basics:

1. **Upload Your Own Documents**: Add your company's actual HR policies
2. **Customize Employee Data**: Edit `data/employee_data.csv` with real data
3. **Adjust Settings**: Modify `config.py` for different behavior
4. **Explore Advanced Features**: Check README.md for full documentation

## 🆘 Need Help?

- Check the full README.md for detailed documentation
- Review the troubleshooting section above
- Verify your API key is valid and has quota remaining
- Make sure all files are in the correct locations

---

**Enjoy using HR Copilot! 🎉**
