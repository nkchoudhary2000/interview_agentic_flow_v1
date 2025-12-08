# Complete Setup Guide - Django Groq Chatbot

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Getting Groq API Key](#getting-groq-api-key)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Usage Guide](#usage-guide)
7. [Troubleshooting](#troubleshooting)

---

## System Requirements

- Python 3.8 or higher
- Windows/Linux/Mac
- Internet connection
- Web browser

---

## Installation

### Step 1: Create Virtual Environment

```bash
# Navigate to project directory
cd "d:\NIOM\Codex project\interview_agentic_flow_v1"

# Create virtual environment
python -m venv venv
```

### Step 2: Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Django 4.2
- Groq AI library
- PDF processing libraries (PyPDF2, pdfplumber)
- Data analysis (pandas)
- Other utilities

---

## Getting Groq API Key

### Why Groq?
- ✅ **100% FREE** - No credit card required
- ✅ **Super Fast** - 10x faster than other APIs
- ✅ **Generous Limits** - 14,400 requests/day
- ✅ **Easy Setup** - Takes 30 seconds

### Steps to Get API Key:

1. **Visit Groq Console**
   - Go to: https://console.groq.com/

2. **Sign Up/Login**
   - Click "Sign in" or "Sign up"
   - Use Google or GitHub (fastest)
   - No forms to fill!

3. **Create API Key**
   - Click "API Keys" in left sidebar
   - Click "Create API Key" button
   - Give it a name: "Django Chatbot"
   - Click "Submit"

4. **Copy Your Key**
   - Copy the entire key (starts with `gsk_...`)
   - ⚠️ **Important:** Save it now - you won't see it again!

---

## Configuration

### Step 1: Create .env File

```bash
# Copy the example file
copy .env.example .env
```

### Step 2: Edit .env File

Open `.env` in any text editor and update:

```env
GROQ_API_KEY=gsk_paste_your_actual_key_here
DEBUG=True
SECRET_KEY=django-insecure-change-this-in-production-12345
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Important Notes:**
- ✅ NO spaces around `=`
- ✅ NO quotes around the key
- ✅ Key should start with `gsk_`
- ✅ Save the file!

### Step 3: Database Setup

```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

Follow prompts to create username and password.

---

## Running the Application

### Start Development Server

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Access the Application

Open your browser and go to:
```
http://localhost:8000
```

### Access Admin Panel (Optional)

```
http://localhost:8000/admin
```

Login with the superuser credentials you created.

---

## Usage Guide

### 1. Code Generation

**How to use:**
1. Type your request in the chat box
2. Example: "Write a Python function to calculate fibonacci numbers"
3. The chatbot will:
   - Generate the code
   - Review it for quality and security
   - Save it to `generated_code/` folder
   - Show you both code and review

**Tips:**
- Be specific about what you want
- Mention the programming language
- Specify any special requirements

**Examples:**
```
"Write a JavaScript function to validate email addresses"
"Create a Python class for managing a todo list"
"Generate SQL query to find top 10 customers by sales"
```

### 2. PDF Text Extraction

**How to use:**
1. Click the file upload area or drag & drop a PDF
2. The chatbot will:
   - Extract all text from the PDF
   - Generate an AI summary
   - Save text to `raw_text/` folder
   - Show statistics (pages, words)

**Supported:**
- ✅ Text-based PDFs
- ✅ Multi-page documents
- ✅ Any file size (larger files take longer)

**Not supported:**
- ❌ Password-protected PDFs
- ❌ Scanned images (OCR not included)

### 3. CSV Analysis

**How to use:**
1. Upload a CSV file
2. The chatbot will:
   - Analyze the structure
   - Understand what data it contains
   - Provide 4-5 smart suggestions
   - Display suggestions as clickable cards

3. Click any suggestion to execute it

**Examples of suggestions:**
- Visualize data distribution
- Check data quality
- Analyze trends
- Export filtered data
- Generate summary reports

---

## Troubleshooting

### Error: "GROQ_API_KEY not found"

**Cause:** API key not in `.env` file or server not restarted

**Solution:**
1. Check `.env` file exists
2. Verify `GROQ_API_KEY=gsk_xxx` is on first line
3. No spaces around `=`
4. **Restart the server** (Ctrl+C, then `python manage.py runserver`)

---

### Error: "Invalid API key"

**Cause:** Incorrect or incomplete API key

**Solution:**
1. Check key starts with `gsk_`
2. Verify you copied the entire key
3. Get a fresh key from console.groq.com
4. Paste in `.env` without quotes or spaces

---

### Error: "No module named 'groq'"

**Cause:** Groq library not installed

**Solution:**
```bash
pip install groq
```

---

### Error: "No module named 'django'"

**Cause:** Virtual environment not activated

**Solution:**
```bash
# Activate virtual environment first
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Then run server
python manage.py runserver
```

---

### Static Files Not Loading

**Cause:** CSS/JS files not collected

**Solution:**
```bash
python manage.py collectstatic
```

---

### Database Errors

**Cause:** Migrations not applied

**Solution:**
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### Server Won't Start (Port in Use)

**Cause:** Another process using port 8000

**Solution:**
```bash
# Use different port
python manage.py runserver 8001

# Or find and kill process using port 8000
netstat -ano | findstr :8000
```

---

### Slow Response Times

**This is normal for:**
- First request after starting server (2-3 seconds)
- Code generation with review (3-5 seconds)
- Large PDF files (depends on size)
- Complex CSV analysis (2-4 seconds)

**Groq is still 5-10x faster than other AI APIs!**

---

## Directory Structure

```
interview_agentic_flow_v1/
├── agents/              # AI agent logic
├── chatbot/            # Django app
├── config/             # Django settings
├── static/             # CSS & JavaScript
├── media/              # User uploads
├── generated_code/     # AI-generated code files
├── raw_text/          # Extracted PDF text
├── venv/              # Virtual environment
├── db.sqlite3         # Database
├── manage.py          # Django management
├── requirements.txt   # Dependencies
├── .env              # Your API keys (DO NOT COMMIT!)
└── .env.example      # Template
```

---

## Performance Tips

1. **Keep server running** - Restarts take 2-3 seconds
2. **Large files** - Upload in chunks if possible
3. **Multiple requests** - Groq handles 30/minute easily
4. **Database** - Grows over time, backup regularly

---

## Security Best Practices

1. **Never commit `.env`** - It's in .gitignore
2. **Change SECRET_KEY** - Use a random string in production
3. **Set DEBUG=False** - In production environments
4. **Use HTTPS** - For production deployment
5. **Regular backups** - Of database and uploaded files

---

## Next Steps

### Customize
- Edit `static/css/chatbot.css` for UI changes
- Modify `agents/` files to change AI behavior
- Update `chatbot/templates/` for HTML changes

### Deploy
- Set up PostgreSQL database
- Configure web server (Nginx/Apache)
- Use gunicorn for production
- Set up SSL certificates

### Enhance
- Add more file types
- Implement data visualization
- Add user authentication
- Create API documentation

---

## Need More Help?

- **README.md** - Overview and quick start
- **GROQ_API_KEY_SETUP.md** - Detailed API key guide
- **Django Docs** - https://docs.djangoproject.com/
- **Groq Docs** - https://console.groq.com/docs

---

**Enjoy your AI-powered chatbot!** 🚀

Built with ❤️ using Django + Groq
