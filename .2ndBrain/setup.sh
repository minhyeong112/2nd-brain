#!/bin/bash
# Second Brain - Automated Setup Script
# Run this after cloning the repo to set up your environment

set -e  # Exit on error

echo "=========================================="
echo "🧠 Second Brain - Setup"
echo "=========================================="
echo ""

# ============================================================
# 1. Check Prerequisites
# ============================================================

echo "📋 Step 1/7: Checking prerequisites..."
echo ""

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "   Install from: https://www.python.org/downloads/"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "✅ $PYTHON_VERSION"

# Check for Python 3.9.x (required for WhisperX compatibility)
PYTHON_MINOR=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ ! "$PYTHON_MINOR" =~ ^3\.9 ]]; then
    echo ""
    echo "⚠️  WARNING: Python 3.9.x is recommended for this project"
    echo "   Current version: $PYTHON_VERSION"
    echo "   Recommended: Python 3.9.6"
    echo ""
    echo "   Why? WhisperX is unmaintained and works best with Python 3.9.x"
    echo "   Newer Python versions (3.10+) may show deprecation warnings."
    echo ""
    echo "   To install Python 3.9.6 with pyenv:"
    echo "   1. Install pyenv: brew install pyenv (macOS)"
    echo "   2. Install Python 3.9.6: pyenv install 3.9.6"
    echo "   3. Set for this project: pyenv local 3.9.6"
    echo "   4. Re-run this setup script"
    echo ""
    # Check if running interactively
    if [ -t 0 ]; then
        read -p "   Continue anyway? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Setup cancelled."
            exit 1
        fi
    else
        echo "   Continuing in non-interactive mode..."
    fi
fi

# Check ffmpeg (for audio processing)
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  ffmpeg not found"
    echo "   Install with: brew install ffmpeg (macOS)"
    echo "   Or: sudo apt install ffmpeg (Linux)"
    exit 1
fi
echo "✅ ffmpeg found"

# Check tesseract (for OCR)
if ! command -v tesseract &> /dev/null; then
    echo "⚠️  tesseract not found"
    echo "   Install with: brew install tesseract (macOS)"
    echo "   Or: sudo apt install tesseract-ocr (Linux)"
    exit 1
fi
echo "✅ tesseract found"

echo ""

# ============================================================
# 2. Create Virtual Environment
# ============================================================

echo "📦 Step 2/7: Creating virtual environment..."
echo ""

if [ -d ".venv" ]; then
    echo "⚠️  Virtual environment already exists"
    # Check if running interactively
    if [ -t 0 ]; then
        read -p "   Recreate it? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf .venv
            python3 -m venv .venv
            echo "✅ Virtual environment recreated"
        else
            echo "⏭️  Skipping virtual environment creation"
        fi
    else
        # Non-interactive mode: Keep existing venv
        echo "⏭️  Skipping virtual environment creation (non-interactive mode)"
    fi
else
    python3 -m venv .venv
    echo "✅ Virtual environment created"
fi

echo ""

# ============================================================
# 3. Activate Virtual Environment & Install Dependencies
# ============================================================

echo "📥 Step 3/7: Installing Python dependencies..."
echo "   (This may take 5-10 minutes, especially for PyTorch and WhisperX)"
echo "   Installing quietly to avoid overwhelming output..."
echo ""

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip (silently)
pip install --upgrade pip > /dev/null 2>&1

# Install dependencies quietly (only show errors)
echo "   ⏳ Installing packages... (this will take several minutes)"
pip install --quiet -r .2ndBrain/requirements.txt 2>&1 | grep -E "(ERROR|error|failed|Failed)" || true

echo ""
echo "✅ Dependencies installed"
echo ""

# ============================================================
# 4. Create Folder Structure
# ============================================================

echo "📁 Step 4/7: Creating folder structure..."
echo ""

# Create main folders if they don't exist
mkdir -p 1-Raw/{m4a,json,md,pdf,jpeg}
mkdir -p 2-Lists
mkdir -p 3-Memos
mkdir -p 4-Wisdom
mkdir -p .chroma

echo "✅ Folders created:"
echo "   1-Raw/ (m4a, json, md, pdf, jpeg)"
echo "   2-Lists/"
echo "   3-Memos/"
echo "   4-Wisdom/"
echo "   .chroma/ (vector database)"
echo ""

# ============================================================
# 5. Set Up Environment Variables
# ============================================================

echo "🔑 Step 5/7: Setting up environment variables..."
echo ""

if [ -f ".env" ]; then
    echo "✅ .env file already exists"
else
    cp .2ndBrain/.env.example .env
    echo "📝 Created .env file from template"
    echo ""
    echo "⚠️  IMPORTANT: You need to add your HuggingFace token"
    echo "   1. Get token: https://huggingface.co/settings/tokens"
    echo "   2. Create token with 'read' access"
    echo "   3. Edit .env file and replace 'your_huggingface_token_here'"
    echo ""
    # Check if running interactively
    if [ -t 0 ]; then
        read -p "   Open .env file now? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            ${EDITOR:-nano} .env
        fi
    else
        echo "   (Run in interactive mode to edit .env)"
    fi
fi

echo ""

# ============================================================
# 6. Initialize Vector Database
# ============================================================

echo "🗄️  Step 6/7: Initializing vector database..."
echo ""

# Check if .chroma has any content
if [ -d ".chroma/chroma.sqlite3" ]; then
    echo "✅ Vector database already initialized"
else
    # Run the init script to create empty database
    python3 .2ndBrain/skills/init-vector-db.py
    echo "✅ Empty vector database created"
fi

echo ""

# ============================================================
# 7. Final Instructions
# ============================================================

echo "✅ Setup complete!"
echo ""
echo "=========================================="
echo "📝 Next Steps"
echo "=========================================="
echo ""
echo "1. VERIFY HUGGINGFACE TOKEN:"
echo "   Edit .env and add your HF_TOKEN"
echo ""
echo "2. START USING:"
echo "   Tell your AI: 'Read .2ndBrain/AI-SETUP.md and execute'"
echo "   Or for daily use: 'Read .2ndBrain/AI-WORKFLOW.md and execute'"
echo ""
echo "=========================================="
echo "📚 Documentation"
echo "=========================================="
echo ""
echo ".2ndBrain/AI-WORKFLOW.md - Daily workflow (for AI)"
echo ".2ndBrain/AI-SETUP.md    - First-time setup (for AI)"
echo ""
echo "🎉 Your Second Brain is almost ready!"
echo "   Let your AI assistant complete the final steps."
echo ""

# Deactivate virtual environment
deactivate
