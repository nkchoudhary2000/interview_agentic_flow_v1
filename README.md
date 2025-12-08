# Django ADK Chatbot with Groq API

A modern, intelligent chatbot system powered by Django and Groq's lightning-fast AI API. Features smart agentic modes for code generation, PDF text extraction, and CSV analysis with human-in-the-loop interactions.

## ⚡ Why Groq?

- **100% FREE** - No credit card needed
- **10x FASTER** - Lightning-fast responses (0.5-2 seconds)
- **Easy Setup** - Get API key in 30 seconds
- **No Quotas** - 14,400 requests/day free tier
- **Powerful** - Llama 3.3 70B model

## Features

### 🤖 Smart Modes

1. **Code Generation Mode** 💻
   - Generate code from natural language prompts
   - Automatic code review and quality analysis
   - Save code directly to `generated_code/` folder
   - Template-based prompt engineering

2. **PDF Extraction Mode** 📄
   - Upload PDF files
   - Extract and save text to `raw_text/` folder
   - AI-powered summaries
   - Statistics (pages, word count)

3. **CSV Analysis Mode** 📊
   - Upload CSV files
   - Intelligent content summarization
   - Smart suggestions for data operations
   - Human-in-the-loop action selection

## Quick Start

### 1. Installation

```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Get FREE Groq API Key

1. Visit: **https://console.groq.com/**
2. Sign in with Google/GitHub (10 seconds)
3. Click "API Keys" → "Create API Key"
4. Copy your key (starts with `gsk_...`)

### 3. Configuration

```bash
# Copy environment template
copy .env.example .env
```

Edit `.env` and add your Groq API key:
```env
GROQ_API_KEY=gsk_your_actual_api_key_here
DEBUG=True
SECRET_KEY=django-insecure-change-this-in-production
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 4. Database Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit **http://localhost:8000** to use the chatbot!

## Usage Examples

### Code Generation
```
You: "Write a Python function to validate email addresses"
Bot: [Generates code, reviews it, saves to generated_code/]
```

### PDF Extraction
```
You: [Upload PDF file]
Bot: "Extracted 1,234 words from 5 pages. Saved to raw_text/document.txt"
     "Summary: This document discusses..."
```

### CSV Analysis
```
You: [Upload employee_data.csv]
Bot: "This CSV contains employee information with 500 records.
      Suggestions:
      1. Visualize salary distribution
      2. Analyze department demographics
      3. Check data quality
      4. Export filtered data"
You: [Click suggestion]
Bot: [Executes action]
```

## Project Structure

```
interview_agentic_flow_v1/
├── agents/                 # Groq AI agents
│   ├── router_agent.py    # Main orchestrator
│   ├── code_gen_agent.py  # Code generation
│   ├── pdf_agent.py       # PDF extraction
│   ├── csv_agent.py       # CSV analysis
│   └── tools.py           # File operations
├── chatbot/               # Django app
│   ├── models.py          # Database models
│   ├── views.py           # API endpoints
│   ├── urls.py
│   └── templates/         # HTML templates
├── static/                # CSS & JavaScript
│   ├── css/chatbot.css   # Glassmorphism UI
│   └── js/chatbot.js     # Frontend logic
├── config/                # Django settings
├── generated_code/        # AI-generated code
├── raw_text/             # Extracted PDF text
├── media/                # Uploaded files
├── manage.py             # Django CLI
├── requirements.txt      # Dependencies
└── .env                  # API keys (create this!)
```

## Technology Stack

- **Backend**: Django 4.2, Django REST Framework
- **AI API**: Groq (Llama 3.3 70B)
- **PDF Processing**: PyPDF2, pdfplumber
- **Data Analysis**: pandas
- **Frontend**: Vanilla JavaScript, Modern CSS

## API Endpoints

- `POST /api/chat/sessions/` - Create new chat session
- `POST /api/chat/message/` - Send message to chatbot
- `POST /api/chat/upload/` - Upload files (PDF/CSV)
- `GET /api/chat/sessions/<id>/messages/` - Get chat history
- `POST /api/chat/action/` - Execute CSV actions

## Features in Detail

### Stunning UI
- Dark theme with vibrant gradients
- Glassmorphism effects
- Smooth animations
- Responsive design
- Drag-and-drop file uploads
- Real-time typing indicators

### Smart Agent Routing
- Automatic intent detection
- Context-aware responses
- Specialized agents for different tasks
- Error handling and fallbacks

### File Handling
- Automatic file type detection
- Processing status tracking
- Result storage in database
- Clean directory structure

## Development

### Running Tests
```bash
python manage.py test
```

### Admin Panel
Access at `http://localhost:8000/admin` to:
- View chat sessions
- Monitor agent executions
- Manage uploaded files
- Debug issues

## Troubleshooting

### "GROQ_API_KEY not found"
- Make sure `.env` file exists
- Check `GROQ_API_KEY=gsk_xxx` is on first line
- No spaces around `=`
- Restart Django server after adding key

### Static files not loading
```bash
python manage.py collectstatic
```

### Database errors
```bash
python manage.py migrate --run-syncdb
```

### Slow responses
- First request may take 2-3 seconds
- Subsequent requests are faster
- PDF/CSV processing takes time for large files

## Performance

- **Basic chat**: < 1 second
- **Code generation**: 1-3 seconds
- **PDF extraction**: 2-5 seconds (depends on file size)
- **CSV analysis**: 2-4 seconds

Groq is **5-10x faster** than other AI APIs!

## Tips for Best Results

### Code Generation
- Be specific: "Write a Python function to validate emails using regex with error handling"
- Mention language: "Create a JavaScript function..."
- Specify requirements: "Include type hints and docstrings"

### PDF Processing
- Text-based PDFs work best
- Scanned PDFs may have poor quality
- Large files (>20 pages) take longer

### CSV Analysis
- Clear column names help
- First few rows should be representative
- Works with any CSV format

## Security Notes

- Keep `.env` file private (it's in .gitignore)
- Don't commit API keys to version control
- Use environment variables in production
- Enable CSRF protection (already configured)

## Deployment

For production deployment:
1. Set `DEBUG=False` in `.env`
2. Configure proper `SECRET_KEY`
3. Set up PostgreSQL database
4. Configure static file serving
5. Use HTTPS
6. Set proper `ALLOWED_HOSTS`

## Support

For issues or questions:
1. Check documentation in this README
2. Review `QUICKSTART.md` for detailed setup
3. Check `GROQ_API_KEY_SETUP.md` for API key help
4. Enable Django debug mode for error details

## What's New

### v1.0.0 - Groq Integration
- ✅ Migrated from Gemini to Groq API
- ✅ 10x faster responses
- ✅ Better free tier (14,400 req/day)
- ✅ Llama 3.3 70B model
- ✅ No quota issues

## License

MIT License

## Acknowledgments

- Groq for amazing AI infrastructure
- Django for robust web framework
- Llama 3.3 for powerful language model

---

**Ready to build amazing AI-powered features!** 🚀

Get your free Groq API key at: https://console.groq.com/
