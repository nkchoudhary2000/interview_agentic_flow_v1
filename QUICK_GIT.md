# Quick Git Commands - Copy & Paste

## Step 1: Add All Files (Already Initialized!)
```bash
git add .
```

## Step 2: Create First Commit
```bash
git commit -m "Initial commit: Django Groq Chatbot with AI agents

- Implemented 4 AI agents (router, code gen, PDF, CSV)
- Created modern UI with glassmorphism design  
- Set up Django backend with REST API
- Integrated Groq API for fast AI responses
- Added comprehensive documentation"
```

## Step 3: Connect to GitHub (Optional)

### A. Create Repository on GitHub
1. Go to https://github.com
2. Click "New Repository"
3. Name it: `django-groq-chatbot`
4. Don't initialize with README (we already have one!)
5. Click "Create repository"

### B. Link & Push
**Copy these commands from GitHub**, or use:

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/django-groq-chatbot.git
git push -u origin main
```

## Later: Add More Changes
```bash
# After making changes:
git add .
git commit -m "Describe your changes"
git push  # If connected to GitHub
```

---

## ⚠️ IMPORTANT: Files Being Committed

### ✅ What WILL Be Committed (Safe):
- All Python code (`.py` files)
- HTML templates
- CSS and JavaScript
- Documentation (`.md` files)
- `.env.example` (template only - safe!)
- `.gitignore`
- `requirements.txt`
- `setup.bat`

### ❌ What WON'T Be Committed (Protected by .gitignore):
- `.env` (your API key - NEVER committed!)
- `venv/` (virtual environment)
- `db.sqlite3` (your database)
- `media/` (uploads)
- `generated_code/` (output)
- `raw_text/` (output)
- `__pycache__/` (cache)

**This is exactly what you want!** Your secrets are safe! 🔒

---

Check `GIT_GUIDE.md` for complete instructions!
