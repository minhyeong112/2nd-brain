# Setup Guide

**For AI**: Guide user through interactive HuggingFace setup, then automate the rest.

## Step 1: Intro

Say:
```
Hi! I'll help set up your Second Brain (~20 minutes).

I'll guide you through free transcription setup (5 min), 
then automate the technical stuff (15 min).

Ready? (Type 'yes')
```

## Step 2: HuggingFace Setup (Interactive)

### 2a. Create Account

Say:
```
Step 1/3: Create HuggingFace Account

Open: https://huggingface.co/join
Create account, then type 'done'
```

### 2b. Accept Model Terms (CRITICAL)

Say:
```
Step 2/3: Accept Terms for AI Models

Open these links and click "Agree and access repository":

1. https://huggingface.co/pyannote/speaker-diarization-3.1
2. https://huggingface.co/pyannote/segmentation-3.0

Type 'done' when BOTH accepted (transcription won't work without both!)
```

### 2c. Create Token

Say:
```
Step 3/3: Create API Token

Open: https://huggingface.co/settings/tokens

1. Click "New token"
2. Name: "second-brain"
3. Access: "Read"
4. Generate and copy token (starts with "hf_...")

Paste your token here:
```

Capture token, then save:
```bash
echo "HF_TOKEN=<token>" > .env
```

Say:
```
✅ Token saved! Now running automated setup (~15 min)...
```

## Step 3: Check Prerequisites

Check:
```bash
python3 --version  # Need 3.9.6
ffmpeg -version
tesseract --version
```

**If missing:**

macOS:
```bash
brew install python@3.9 ffmpeg tesseract
```

Linux:
```bash
sudo apt install python3 python3-venv ffmpeg tesseract-ocr
```

## Step 4: Run Setup (MANDATORY)

Say:
```
Running setup... Downloads ~2GB AI models (10-15 min)
```

Execute:
```bash
chmod +x .2ndBrain/setup.sh
./.2ndBrain/setup.sh
```

Report progress:
- "✅ Prerequisites checked"
- "✅ Virtual environment created"
- "📥 Installing dependencies (PyTorch, WhisperX...)"
- "✅ Folders created"
- "✅ Vector database initialized"

## Step 5: Verify

Test:
```bash
.venv/bin/python3 .2ndBrain/skills/transcribe.py
.venv/bin/python3 .2ndBrain/skills/semantic-search.py "test"
```

If errors, check HF model terms (step 2b).

## Step 6: Welcome

Say:
```
🎉 Setup Complete!

Installed:
✅ Audio transcription (WhisperX)
✅ Image OCR (Tesseract)
✅ Semantic search (ChromaDB)
✅ Knowledge garden (Lists, Tasks, Memos, Wisdom, etc.)

────────────────────────

📝 RECOMMENDED: Use Obsidian for notes
🤖 Use any AI assistant (OpenCode, Cline, Cursor, etc.)

────────────────────────

🚀 TRY IT:
1. Drop voice memo in folder
2. Say: "process"

Happy thinking! 🧠✨
```

## Troubleshooting

**"HuggingFace auth error"**
→ Accept BOTH model terms (step 2b)

**"ffmpeg not found"**
→ brew install ffmpeg (macOS)

**"Python version wrong"**
→ Need Python 3.9.6 specifically

---

*Last updated: 2026-01-21*
