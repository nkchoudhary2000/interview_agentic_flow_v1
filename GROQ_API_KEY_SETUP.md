# How to Get Your FREE Groq API Key

## Step 1: Visit Groq Console
Go to: **https://console.groq.com/**

## Step 2: Sign Up (FREE - No Credit Card!)
1. Click **"Sign Up"** or **"Get Started"**
2. Sign up with:
   - Google account (easiest), OR
   - GitHub account, OR
   - Email

**Note:** Completely FREE - no payment info needed!

## Step 3: Get Your API Key
1. After logging in, go to **API Keys** section
2. Click **"Create API Key"**
3. Give it a name (e.g., "Django Chatbot")
4. Click **"Create"**
5. **COPY the API key** - it starts with `gsk_...`

**IMPORTANT:** Copy it now! You won't be able to see it again.

## Step 4: Add to Your Project
1. Open your `.env` file in the project root:
   ```
   d:\NIOM\Codex project\interview_agentic_flow_v1\.env
   ```

2. Add this line (replace with your actual key):
   ```
   GROQ_API_KEY=gsk_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

3. Save the file

## Step 5: Install Groq Library
Run this command:
```bash
pip install groq
```

## Step 6: Restart Your Server
1. Stop the Django server (Ctrl+C)
2. Start it again:
   ```bash
   python manage.py runserver
   ```

## Test It!
Go to http://localhost:8000 and try:
- "Write a Python function to add two numbers"
- Upload a PDF file  
- Upload a CSV file

## Why Groq?

✅ **Completely FREE** (no credit card)
✅ **Super FAST** (faster than ChatGPT!)
✅ **Easy to use** (30 seconds to get API key)
✅ **No quota limits** for free tier
✅ **Great models**: Llama 3.3 70B, Mixtral, Gemma

## Groq Free Tier Limits

- **30 requests per minute**
- **14,400 requests per day**
- **7,000 tokens per minute**

This is MORE than enough for development and testing!

## Having Issues?

### Issue: "API key not found"
**Solution:** Make sure you:
1. Added `GROQ_API_KEY=your_key` to `.env`
2. No spaces around the `=`
3. Restarted the Django server

### Issue: "Invalid API key"
**Solution:**
1. Check your key starts with `gsk_`
2. Make sure you copied the entire key
3. Get a new key from Groq console

### Issue: "Module 'groq' not found"
**Solution:**
```bash
pip install groq
```

## Your Current Setup

After completing these steps, your `.env` should look like:

```env
GROQ_API_KEY=gsk_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
DEBUG=True
SECRET_KEY=django-insecure-change-this-in-production-12345
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Ready to Go!

Once you have your Groq API key configured, your chatbot will have:
- 💨 **Lightning-fast responses** (Groq is REALLY fast!)
- 💻 **Code generation** with automatic review
- 📄 **PDF text extraction** with summaries
- 📊 **CSV analysis** with smart suggestions

Enjoy your super-fast, free AI chatbot! 🚀
