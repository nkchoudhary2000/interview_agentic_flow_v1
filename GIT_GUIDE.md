# Git Commit Guide - Django Groq Chatbot

## Quick Git Setup

### Step 1: Initialize Git (if not already done)

```bash
# Navigate to project directory
cd "d:\NIOM\Codex project\interview_agentic_flow_v1"

# Initialize git repository (only if needed)
git init
```

### Step 2: Configure Git (First Time Only)

```bash
# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Check What Will Be Committed

```bash
# See which files will be added
git status
```

### Step 4: Add Files to Staging

```bash
# Add all files (recommended for first commit)
git add .

# Or add specific files only
git add README.md
git add requirements.txt
git add agents/
git add chatbot/
# ... etc
```

### Step 5: Commit Changes

```bash
# Create your first commit
git commit -m "Initial commit: Django Groq Chatbot with AI agents"

# Or with more details
git commit -m "feat: Complete Django chatbot with Groq AI integration

- Implemented 4 AI agents (router, code gen, PDF, CSV)
- Created modern UI with glassmorphism design
- Set up Django backend with REST API
- Added comprehensive documentation
- Configured Groq API integration"
```

### Step 6: Create .gitignore (Already Done!)

Your `.gitignore` already excludes:
- ✅ `.env` (your API keys - NEVER commit this!)
- ✅ `venv/` (virtual environment)
- ✅ `db.sqlite3` (database)
- ✅ `__pycache__/` (Python cache)
- ✅ `media/` (user uploads)
- ✅ Generated files

## Connecting to GitHub

### Option 1: Using GitHub Desktop (Easiest)
1. Download GitHub Desktop: https://desktop.github.com/
2. Open GitHub Desktop
3. Click "Add" → "Add Existing Repository"
4. Select your project folder
5. Click "Publish repository" to GitHub

### Option 2: Using Command Line

**Create a new repository on GitHub first**, then:

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/django-groq-chatbot.git

# Push your code
git branch -M main
git push -u origin main
```

## Important Files to Verify

### ✅ Files That WILL Be Committed (Good):
- All Python files (`.py`)
- Templates (`.html`)
- Static files (`.css`, `.js`)
- Documentation (`.md`)
- Requirements (`requirements.txt`)
- Configuration files
- `.env.example` (template only)
- `.gitignore`

### ❌ Files That WON'T Be Committed (Good - They're in .gitignore):
- `.env` (contains your API key!)
- `venv/` (virtual environment)
- `db.sqlite3` (database with your data)
- `__pycache__/` (Python cache)
- `*.pyc` (compiled Python)
- `media/` (user uploads)
- `generated_code/` (AI-generated files)
- `raw_text/` (extracted text)

## Common Git Commands

### Check Status
```bash
git status
```

### See What Changed
```bash
git diff
```

### View Commit History
```bash
git log --oneline
```

### Add More Changes Later
```bash
# Make your code changes, then:
git add .
git commit -m "Description of changes"
git push  # If connected to GitHub
```

### Create a Branch (For New Features)
```bash
git checkout -b feature-name
# Make changes
git add .
git commit -m "Added feature"
git checkout main
git merge feature-name
```

## Recommended Commit Messages

Use clear, descriptive commit messages:

**Good:**
```
git commit -m "feat: Add CSV export functionality"
git commit -m "fix: Resolve PDF extraction encoding issue"
git commit -m "docs: Update setup guide with Groq instructions"
git commit -m "refactor: Simplify agent routing logic"
```

**Bad:**
```
git commit -m "update"
git commit -m "changes"
git commit -m "fixed stuff"
```

## First Commit Checklist

Before your first commit, verify:

- [ ] `.env` is in `.gitignore` (✅ Already done)
- [ ] No sensitive data in code
- [ ] `venv/` is excluded (✅ Already done)
- [ ] Database is excluded (✅ Already done)
- [ ] Documentation is updated
- [ ] README.md explains the project
- [ ] requirements.txt is current

## Repository Structure (What Will Be on GitHub)

```
django-groq-chatbot/
├── README.md                 ← Project overview
├── SETUP_GUIDE.md           ← Setup instructions
├── GROQ_API_KEY_SETUP.md    ← API key guide
├── DOCUMENTATION.md         ← Docs index
├── requirements.txt         ← Dependencies
├── .env.example            ← Template (safe)
├── .gitignore              ← Git exclusions
├── manage.py               ← Django CLI
├── setup.bat               ← Windows setup
│
├── agents/                 ← AI agents
├── chatbot/               ← Django app
├── config/                ← Settings
└── static/                ← CSS/JS

# NOT included (in .gitignore):
# .env, venv/, db.sqlite3, media/, generated_code/, raw_text/
```

## Troubleshooting

### "git: command not found"
**Install Git:**
- Download from: https://git-scm.com/downloads
- Install with default options
- Restart your terminal

### "Already a git repository"
```bash
# Check existing remotes
git remote -v

# If you want to start fresh
rm -rf .git
git init
```

### "Permission denied (publickey)"
**Use HTTPS instead of SSH:**
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/repo.git
```

### Accidentally Committed .env File?
**Remove it immediately:**
```bash
git rm --cached .env
git commit -m "Remove .env from repository"
git push
```

Then **regenerate your API key** (the old one is now public!)

## Quick Commands Summary

```bash
# First time setup
git init
git add .
git commit -m "Initial commit: Django Groq Chatbot"

# Connect to GitHub (after creating repo there)
git remote add origin https://github.com/YOUR_USERNAME/your-repo.git
git push -u origin main

# Daily workflow
git add .
git commit -m "Your descriptive message"
git push
```

## Next Steps After Committing

1. ✅ Share the GitHub link with others
2. ✅ Add a LICENSE file (MIT, GPL, etc.)
3. ✅ Add badges to README.md
4. ✅ Set up GitHub Actions (optional)
5. ✅ Create releases/tags for versions

---

**Remember:** NEVER commit your `.env` file with API keys! 🔒

The `.gitignore` file already protects you, but double-check with `git status` before committing!
