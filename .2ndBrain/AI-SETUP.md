# Interactive Setup Guide for AI

**For AI (Cline)**: You're guiding a human through their Second Brain setup. Be conversational, patient, and helpful.

**User command**: `Read .2ndBrain/AI-SETUP.md and execute`

---

## 🎯 Your Mission

Walk the user through HuggingFace setup step-by-step, then automate everything else. The user should feel guided, not overwhelmed.

---

## Step 1: Confirm We're Ready

Say to user:

```
Hi! I'm going to help you set up your Second Brain. This takes about 20 minutes total.

I'll guide you through getting a free transcription token, then I'll handle all the technical stuff (Python, models, databases, etc.) while you grab coffee.

Ready to start? (Type 'yes' to continue)
```

Wait for user confirmation.

---

## Step 2: HuggingFace Setup (Interactive - 5 minutes)

### 2a. Introduction

Say to user:

```
First, we need to set up free audio transcription through HuggingFace. This is 100% free and takes 3 minutes.

You'll need to:
1. Create a free account
2. Accept terms for 2 AI models (required for speaker recognition)
3. Create an API token

I'll guide you through each step. Ready? (Type 'yes')
```

Wait for confirmation.

---

### 2b. Create Account

Say to user:

```
Step 1/3: Create HuggingFace Account

Please open this link in your browser:
https://huggingface.co/join

Create your free account, then type 'done' here when you're ready for the next step.
```

Wait for user to type 'done'.

---

### 2c. Accept Model Terms (CRITICAL!)

Say to user:

```
Step 2/3: Accept Terms for AI Models

For speaker recognition to work, you need to accept terms for TWO models.

Please open these links and click "Agree and access repository" on each:

1. https://huggingface.co/pyannote/speaker-diarization-3.1
   (Click the "Agree and access repository" button)

2. https://huggingface.co/pyannote/segmentation-3.0
   (Click the "Agree and access repository" button)

Type 'done' when you've accepted BOTH. (This is important - transcription won't work without both!)
```

Wait for user to type 'done'.

---

### 2d. Create Token

Say to user:

```
Step 3/3: Create Your API Token

Please open this link:
https://huggingface.co/settings/tokens

1. Click "New token"
2. Give it any name (e.g., "second-brain")
3. Select "Read" access
4. Click "Generate token"
5. Copy the token (starts with "hf_...")

IMPORTANT: Keep this token somewhere safe!

Now paste your token here:
```

**Capture the token from user input.** Store it in a variable.

---

### 2e. Save Token

After receiving token, create/update the `.env` file:

```bash
echo "HF_TOKEN=<user_provided_token>" > .env
```

Say to user:

```
✅ Got it! Token saved securely.

Now I'll handle all the technical setup. This takes about 15 minutes.
You can grab coffee while I work! ☕

Starting automated setup...
```

---

## Step 3: Check Prerequisites

**IMPORTANT: This only checks if tools exist. You MUST proceed to Step 4 to create the virtual environment!**

Check if required tools are installed:

```bash
python3 --version  # Need 3.11+
ffmpeg -version    # Audio processing
tesseract --version # OCR
git --version      # Version control
```

**If anything is missing:**

### macOS:
```
I need to install some tools first. Please run these commands in your terminal:

# Install Homebrew (if needed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python@3.11 ffmpeg tesseract git

After installation, tell me 'done' so I can continue.
```

### Linux:
```
I need to install some tools first. Please run:

sudo apt update
sudo apt install python3 python3-venv ffmpeg tesseract-ocr git

After installation, tell me 'done' so I can continue.
```

### Windows:
```
Please install these tools:
- Python 3.11+: https://www.python.org/downloads/
- ffmpeg: https://ffmpeg.org/download.html (add to PATH)
- Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
- Git: https://git-scm.com/downloads

After installation, tell me 'done' so I can continue.
```

**Wait for user to complete installations, then recheck.**

Once all prerequisites pass, say:

```
✅ All system tools are ready!

Now proceeding to Step 4 to create your virtual environment and install dependencies...
```

**DO NOT STOP HERE - Continue immediately to Step 4!**

---

## Step 4: Run Automated Setup Script (CRITICAL - DO NOT SKIP!)

**This step is MANDATORY even if prerequisites are installed!**
**This creates the .venv virtual environment and installs all Python packages!**

Say to user:

```
Running automated setup... This creates your virtual environment and downloads ~2GB of AI models.

This takes 10-15 minutes. I'll report progress as we go!
```

Execute the setup script:

```bash
cd ~/Desktop/2nd-brain
chmod +x .2ndBrain/setup.sh
./.2ndBrain/setup.sh
```

**Monitor the output and report progress to user:**

- "✅ Prerequisites checked..."
- "✅ Virtual environment created..." (KEY STEP - .venv folder created here!)
- "📥 Installing dependencies (this is the slow part - PyTorch, WhisperX, etc.)..."
- "✅ Folder structure created..."
- "✅ Vector database initialized..."

**NOTE:** The script runs in non-interactive mode when executed by AI, so it will:
- Automatically create .venv if it doesn't exist
- Skip .venv recreation if it already exists
- Create .env from template if needed (you already did this in Step 2e)

---

## Step 5: Verify Setup

Run validation tests:

```bash
# Test transcription (should say "No audio files found")
.venv/bin/python3 .2ndBrain/.scripts/transcribe.py

# Test compilation (should say "No files to process")  
.venv/bin/python3 .2ndBrain/.scripts/compile-raw-text.py

# Test semantic search (should work without errors)
.venv/bin/python3 .2ndBrain/.scripts/semantic-search.py "test query"
```

**If any errors occur:**
- Check the error message
- Common issue: HuggingFace model terms not accepted (guide user back to step 2c)
- Report specific error and help troubleshoot

---

## Step 6: Welcome & Next Steps

Say to user:

```
🎉 Setup Complete! Your Second Brain is Ready!

What's installed:
✅ Audio transcription (WhisperX with speaker recognition)
✅ Image OCR (Tesseract)
✅ Semantic search (ChromaDB)
✅ Knowledge garden structure:
   • 1-Raw/ (new thoughts land here)
   • 2-Lists/ (active tasks & ideas)
   • 3-Memos/ (deep thinking documents)
   • 4-Wisdom/ (timeless principles)

────────────────────────────────────

📱 OPEN YOUR SECOND BRAIN IN OBSIDIAN:

Your Second Brain is fully Obsidian-compatible! This is the recommended way to interact with your notes:

1. Open Obsidian on your computer
2. Click "Open folder as vault"
3. Navigate to: ~/Desktop/2nd-brain
4. Click "Open"

Now you can:
• Browse your knowledge garden
• Create and edit notes
• Drop voice memos, photos, and files directly into the folder
• Use Obsidian's graph view to see connections

💡 Optional: Want to sync across devices?
   If you have Obsidian Sync, you can enable it AFTER opening the vault:
   • Open the vault in Obsidian
   • Go to Settings → Sync
   • Connect your Obsidian Sync account
   • Choose to merge or upload the existing vault

────────────────────────────────────

HOW TO USE (Daily Workflow):

1. Drop files in your 2nd-brain folder (via Obsidian or Finder):
   - Voice memos (.m4a, .mp3, .wav)
   - Photos (.jpg, .png)
   - Notes (.md)
   - PDFs

2. Open VS Code in this folder, then tell me:
   "Read .2ndBrain/AI-Workflow.md and process"

3. I'll:
   ✅ Transcribe audio
   ✅ Extract text from images
   ✅ Review everything with you
   ✅ Organize into your knowledge garden
   ✅ Update search index

You approve at key steps. I do the heavy lifting.

────────────────────────────────────

Want to try it now? Drop a voice memo or photo in your Obsidian vault, 
then open VS Code and tell me:
"Read .2ndBrain/AI-Workflow.md and process"

Or just say: "process"

Happy thinking! 🧠✨
```

---

## 🔒 Important Notes

### Privacy
- Never log or share the HF_TOKEN
- User's notes stay local (not in Git)
- Only transcription uses HuggingFace API

### Error Handling
- Be patient and clear with error messages
- Most common issue: Model terms not accepted on HuggingFace
- Guide user calmly through fixes

### Time Expectations
- HuggingFace setup: 3-5 minutes (user active)
- Automated setup: 15-20 minutes (user can leave)
- Total: ~20 minutes

---

## Troubleshooting Quick Reference

**"HuggingFace authentication error"**
→ User needs to accept BOTH model terms (step 2c)
→ Go to links and click "Agree and access repository"

**"ffmpeg not found"**
→ brew install ffmpeg (macOS)
→ sudo apt install ffmpeg (Linux)

**"Python version too old"**
→ Need Python 3.11+
→ brew install python@3.11 (macOS)

**"WhisperX installation failed"**
→ Upgrade pip first: `.venv/bin/python3 -m pip install --upgrade pip`
→ Try again

---

*This setup runs once. After completion, user will use AI-WORKFLOW.md for daily operations.*

*Setup guide last updated: 2026-01-07*
