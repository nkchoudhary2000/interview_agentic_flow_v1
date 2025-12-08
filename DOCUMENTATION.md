# Project Documentation Index

## 📚 Available Documentation

### 1. **README.md** - Start Here!
**What it covers:**
- Project overview
- Quick start guide
- Features and capabilities
- Technology stack
- Basic usage examples

**Read this first!**

---

### 2. **SETUP_GUIDE.md** - Complete Setup Instructions
**What it covers:**
- Detailed installation steps
- Groq API key setup
- Configuration guide
- Database setup
- Troubleshooting common issues
- Usage examples for all features

**Read this for detailed setup!**

---

### 3. **GROQ_API_KEY_SETUP.md** - API Key Help
**What it covers:**
- How to get FREE Groq API key
- Step-by-step instructions
- Troubleshooting API key issues
- Why Groq is better than alternatives

**Read this if you need help with the API key!**

---

## 🚀 Quick Reference

### First Time Setup
1. Read **README.md** sections 1-5
2. Follow **SETUP_GUIDE.md** installation
3. Get API key using **GROQ_API_KEY_SETUP.md**
4. Run `python manage.py runserver`
5. Visit http://localhost:8000

### Having Issues?
- Check **SETUP_GUIDE.md** → Troubleshooting section
- Review **GROQ_API_KEY_SETUP.md** → Having Issues section

### Want to Understand the Code?
- Read **README.md** → Project Structure
- Explore the `agents/` directory
- Check `chatbot/views.py` for API logic

---

## 📁 Project Structure

```
interview_agentic_flow_v1/
├── 📄 README.md              ← Overview & quick start
├── 📄 SETUP_GUIDE.md         ← Complete setup instructions
├── 📄 GROQ_API_KEY_SETUP.md  ← API key help
├── 📄 requirements.txt       ← Python dependencies
├── 📄 manage.py              ← Django management
├── 📄 .env.example           ← Environment template
├── 📄 .env                   ← Your config (create this!)
│
├── 📂 agents/                ← AI agent logic
│   ├── router_agent.py       ← Main orchestrator
│   ├── code_gen_agent.py     ← Code generation
│   ├── pdf_agent.py          ← PDF extraction
│   ├── csv_agent.py          ← CSV analysis
│   └── tools.py              ← File operations
│
├── 📂 chatbot/               ← Django app
│   ├── models.py             ← Database models
│   ├── views.py              ← API endpoints
│   ├── urls.py               ← URL routing
│   ├── admin.py              ← Admin config
│   └── templates/            ← HTML files
│
├── 📂 config/                ← Django settings
│   ├── settings.py           ← Main configuration
│   └── urls.py               ← Root URLs
│
├── 📂 static/                ← Frontend assets
│   ├── css/chatbot.css       ← Styling
│   └── js/chatbot.js         ← JavaScript
│
├── 📂 generated_code/        ← AI-generated code output
├── 📂 raw_text/              ← Extracted PDF text
├── 📂 media/                 ← User uploads
├── 📂 venv/                  ← Virtual environment
└── 📄 db.sqlite3             ← Database
```

---

## 🎯 What to Read When

### "I just want to get started quickly"
→ **README.md** Quick Start section (5 minutes)

### "I want complete setup instructions"
→ **SETUP_GUIDE.md** full guide (15 minutes)

### "I'm stuck on the API key"
→ **GROQ_API_KEY_SETUP.md** (5 minutes)

### "Something's not working"
→ **SETUP_GUIDE.md** → Troubleshooting section

### "I want to customize the chatbot"
→ **README.md** → Project Structure
→ Explore `agents/` and `chatbot/` folders

---

## ✅ Documentation Checklist

Before asking for help, make sure you've:

- [ ] Read README.md Quick Start
- [ ] Followed SETUP_GUIDE.md installation steps
- [ ] Got your Groq API key from console.groq.com
- [ ] Added GROQ_API_KEY to .env file
- [ ] Restarted Django server after config changes
- [ ] Checked Troubleshooting sections

---

## 🔗 External Resources

- **Groq Console**: https://console.groq.com/
- **Groq Documentation**: https://console.groq.com/docs
- **Django Docs**: https://docs.djangoproject.com/
- **Python Docs**: https://docs.python.org/

---

**Everything you need is in these 3 files!** 📚

Start with README.md → Move to SETUP_GUIDE.md → Done! 🎉
