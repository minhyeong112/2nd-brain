# AI Agent Guidelines for Second Brain

**Purpose**: This document provides AI coding assistants with essential information for working in this repository.

**For AI Agents**: Read this file before making changes to understand commands, code style, and workflow.

**Tool Compatibility**: This system works with any AI coding assistant (OpenCode, Cline, Cursor, etc.) and any markdown editor (Obsidian, VS Code, Vim, etc.). OpenCode + Obsidian are recommended for optimal experience.

---

## 🎯 Project Overview

**Second Brain** is a personal knowledge management system that:
- Transcribes voice memos using WhisperX with speaker diarization
- Performs OCR on images using Tesseract
- Provides semantic search across notes using ChromaDB
- Organizes knowledge in a compression-based structure (Raw → Lists → Memos → Wisdom)
- Fully compatible with Obsidian for note editing

**Tech Stack**: Python 3.9.6, WhisperX, ChromaDB, Tesseract, FFmpeg

---

## 🚀 Workflow Commands

### When User Says "process" (or similar)

If the user says any of these:
- "process"
- "process my files"
- "execute workflow"
- "run the workflow"

**YOU MUST IMMEDIATELY**:

1. **Read** `.2ndBrain/AI-WORKFLOW.md` using the Read tool
2. **Execute the complete workflow** described in that file, following ALL steps in order
3. **Do not skip any steps**, including:
   - Mandatory semantic search before every recommendation
   - Hard stops for human approval (after RAW-TEXT.md and PROCESSING-PLAN.md)
   - File cleanup and re-indexing at the end

The workflow file contains the detailed step-by-step instructions for processing files. **Always read it first** before starting any processing work.

### When User Says "setup" (or similar)

If the user says any of these:
- "setup"
- "initial setup"
- "first time setup"
- "install"

**Read and execute**: `.2ndBrain/AI-SETUP.md`

This contains the interactive setup guide for first-time installation.

---

## 🎯 Quick Reference Commands

### Python Environment

**CRITICAL**: Always use the virtual environment Python:
```bash
/Users/mig/Desktop/code/2nd\ Brain/.venv/bin/python3 <script>
```

**Never** use system Python (`python3` or `python`). The venv ensures all dependencies are available.

### Core Workflow Commands

```bash
# Transcribe audio files (MUST run first if .m4a files exist)
.venv/bin/python3 .2ndBrain/skills/transcribe.py

# Compile raw text from all sources (requires human approval)
.venv/bin/python3 .2ndBrain/skills/compile-raw-text.py

# Semantic search (use for planning - MANDATORY before recommendations)
.venv/bin/python3 .2ndBrain/skills/semantic-search.py "query text"

# Re-index a single file after modifications
.venv/bin/python3 .2ndBrain/skills/embed-note.py "path/to/file.md"

# Re-index all files (use sparingly)
.venv/bin/python3 .2ndBrain/skills/init-vector-db.py

# Approve processing plan (interactive)
.venv/bin/python3 .2ndBrain/skills/approve-processing-plan.py
```

### Setup Commands

```bash
# Initial setup (creates venv, installs dependencies)
./.2ndBrain/setup.sh

# Check Python version
python3 --version  # Should be 3.9.6

# Verify dependencies
.venv/bin/python3 -m whisperx --version
ffmpeg -version
tesseract --version
```

---

## 📋 Code Style Guidelines

### Python

**Imports**:
- Standard library imports first
- Third-party imports second
- Local imports last
- Alphabetize within groups
- Use absolute imports

Example:
```python
import os
import sys
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
```

**Formatting**:
- 4 spaces for indentation (no tabs)
- Max line length: 120 characters (flexible for readability)
- Double quotes for strings (consistent with existing code)
- Add blank line between function definitions
- Use descriptive variable names (no single letters except loop counters)

**Types**:
- Type hints not currently used but acceptable for new complex functions
- Docstrings for all public functions and modules
- Use triple double quotes for docstrings

**Functions**:
- Descriptive names in snake_case
- Keep functions focused and single-purpose
- Extract complex logic into helper functions
- Document what, not how (code should be self-documenting)

Example:
```python
def preprocess_audio(input_file, output_file):
    """Preprocess audio to 16kHz mono WAV and trim silences."""
    # Implementation...
```

**Error Handling**:
- Use descriptive error messages with emoji indicators (❌, ⚠️)
- Exit with code 1 on failure, 0 on success
- Print errors to stderr using `file=sys.stderr`
- Validate prerequisites early (fail fast)
- Clean up temporary files in all code paths

Example:
```python
if not HF_TOKEN or HF_TOKEN == 'your_huggingface_token_here':
    print("❌ Error: HuggingFace token not configured")
    print("   Please edit .env file and add your HF_TOKEN")
    exit(1)
```

**User Feedback**:
- Use emoji for visual clarity (🎵, ✅, ❌, 🔍, 📝, ⚠️, ⏭️)
- Show progress for long operations
- Report time elapsed for lengthy tasks
- Provide next steps in success messages

**File Operations**:
- Use `Path` from pathlib for all file operations
- Quote file paths in shell commands to handle spaces
- Check file existence before operations
- Use context managers (`with`) for file I/O

---

## 🔧 Development Guidelines

### Adding New Skills

1. Place in `.2ndBrain/skills/`
2. Add shebang: `#!/usr/bin/env python3`
3. Add module docstring with usage
4. Make executable: `chmod +x script.py`
5. Follow existing code style
6. Update this file with new commands

### Modifying Existing Scripts

1. Read the entire script first
2. Maintain existing style and patterns
3. Test with sample data
4. Verify cleanup happens correctly
5. Update documentation if behavior changes

### Working with Vector Database

**When to re-index**:
- After creating new notes
- After modifying note content
- After moving/renaming notes

**Re-index command**:
```bash
.venv/bin/python3 .2ndBrain/skills/embed-note.py "path/to/modified/file.md"
```

**Database location**: `.chroma/` (at repository root, gitignored)

---

## 🗂️ Repository Structure

Hidden folders represent different technologies/systems:

```
2nd Brain/
├── .2ndBrain/               # Second Brain system (committed)
│   ├── skills/             # Python skills (transcribe, search, embed, etc.)
│   ├── AI-WORKFLOW.md      # Daily operations guide
│   ├── AI-SETUP.md         # Initial setup guide
│   ├── setup.sh            # Automated setup
│   └── requirements.txt    # Python dependencies
├── .opencode/               # OpenCode config (optional, committed)
│   └── opencode.json       # Permission settings
├── .obsidian/               # Obsidian config (optional, committed)
│   └── app.json            # File visibility settings
├── .venv/                   # Python virtual environment (gitignored)
├── .chroma/                 # Vector database (gitignored)
├── .Archive/                # Historical source files (gitignored)
│   ├── m4a/                # Audio files
│   ├── json/               # Transcriptions
│   ├── md/                 # Markdown sources
│   ├── pdf/                # Documents
│   └── jpeg/               # Images
├── Lists/                   # Active working knowledge (gitignored)
├── Memos/                   # Deep thinking documents (gitignored)
├── Wisdom/                  # Life principles (gitignored)
├── Conversations/           # Discussion notes (gitignored)
├── Tasks/                   # Task management by category (gitignored)
├── Shopping/                # Shopping lists by category (gitignored)
├── Contacts/                # Contact lists by category (gitignored)
└── AGENTS.md               # This file (committed)
```

**Root directory**: Should be clean except folders and temp processing files during active sessions.

**Tool Flexibility**: 
- `.opencode/` and `.obsidian/` are optional - use any editor/AI assistant you prefer
- The core system (`.2ndBrain/`) works independently of specific tools

## 🎯 Organization Principle: One Layer Deep

**CRITICAL**: All notes must remain **one layer deep** - no subheadings or sublists within documents.

**Why**: This enforces atomic, focused notes and prevents hierarchical complexity.

**Examples**:
- ❌ Bad: Shopping.md with subheadings for "Groceries", "Hardware", "Clothing"
- ✅ Good: Separate notes - Shopping-Groceries.md, Shopping-Hardware.md, Shopping-Clothing.md

- ❌ Bad: Tasks.md with nested task categories and sublists
- ✅ Good: Separate task files - Tasks-Urgent.md, Tasks-Admin.md, Tasks-Health.md

- ❌ Bad: Contacts.md with subheadings for different contact types
- ✅ Good: Separate contact files - Contacts-Healthcare.md, Contacts-Korea.md, Contacts-Business-Professional.md

**When creating/updating notes**: Always maintain flat structure. If a note needs subsections, create separate notes instead.

### Adding New Items to Categorized Folders

**For Tasks, Shopping, and Contacts**: When adding new items, follow this process:

1. **Search for existing category**: Use semantic search to find relevant category files
2. **Add to existing file if appropriate**: If the item fits an existing category, add it there
3. **Create new category file if needed**: If no existing category fits, create a new one following the naming convention
   - Example: New urgent task → `Tasks-Urgent.md`
   - Example: New electronics shopping item → `Shopping-Electronics-Tech.md`
   - Example: New legal contact → `Contacts-Legal.md`

**Do NOT**: Add sublists or subheadings within a single file. Always create separate category files to maintain the one-layer-deep principle.

---

## ⚠️ Critical Workflow Rules

### Mandatory Semantic Search

**BEFORE** recommending any action, you MUST:
1. Search for related content: `.venv/bin/python3 .2ndBrain/skills/semantic-search.py "relevant query"`
2. Review results to understand existing structure
3. Make informed recommendations based on what exists

**Never assume** - always search first.

### Processing Order (Strict)

1. **Transcribe audio** (if .m4a files exist) - MUST complete first
2. **Compile raw text** - waits for human typing "approved"
3. **Create PROCESSING-PLAN.md** - using semantic search for EVERY item
4. **Wait for approval** - human types "approved" or runs approval script
5. **Execute changes** - update/create files as specified
6. **Re-index modified files** - update vector database
7. **Clean up root** - move all files to appropriate .Archive/ subdirectories

**DO NOT skip steps** or proceed without approvals.

### Hard Stops (Human Review Required)

1. After `compile-raw-text.py` - Human reviews RAW-TEXT.md, fixes transcription errors, types "approved"
2. After creating PROCESSING-PLAN.md - Human reviews plan, types "approved" or runs approval script

**These stops are enforced by scripts** - don't bypass them.

### File Movement (Step 7)

After executing changes, AI **MUST** clean root:
- Audio files (.m4a) → `.Archive/m4a/`
- JSON files (.json) → `.Archive/json/`
- Markdown files (.md) → `.Archive/md/` (including Untitled.md, RAW-TEXT.md, PROCESSING-PLAN.md, *-ocr.md)
- Temporary files (temp_*.wav) → delete

**Verify**: Only folders should remain in root (.Archive/, Lists/, Memos/, Wisdom/, Conversations/, Tasks/, Shopping/, Contacts/, hidden folders)

---

## 📝 Naming Conventions

**Files**:
- Scripts: `kebab-case.py` (e.g., `semantic-search.py`)
- Notes: `Title-Case.md` (e.g., `App-Ideas.md`, `Discussion-with-James.md`)
- Processing artifacts: `UPPERCASE.md` (e.g., `RAW-TEXT.md`, `PROCESSING-PLAN.md`)
- **Categorized files**: `Category-Subcategory.md` format
  - Tasks: `Tasks-[Category].md` (e.g., `Tasks-Urgent.md`, `Tasks-Admin.md`, `Tasks-Health.md`)
  - Shopping: `Shopping-[Category].md` (e.g., `Shopping-Groceries.md`, `Shopping-Miami.md`)
  - Contacts: `Contacts-[Category].md` (e.g., `Contacts-Healthcare.md`, `Contacts-Korea.md`)

**Variables**:
- Python: `snake_case` (e.g., `hf_token`, `audio_file`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `HF_TOKEN`)

**Functions**:
- Python: `snake_case` (e.g., `preprocess_audio`, `semantic_search`)

---

## 🔐 Security & Privacy

- **Never** commit `.env` file (contains HF_TOKEN)
- **Never** commit personal notes (.Archive/, Lists/, Memos/, Wisdom/, Conversations/, Tasks/)
- **Never** log or display API tokens
- **Never** commit `.chroma/` database (personal note embeddings)
- `.gitignore` is carefully configured - don't modify without review

---

## 🎓 Common Patterns

### Path Handling

```python
from pathlib import Path

# Get base path (repository root)
base_path = Path(__file__).parent.parent.parent
root_dir = Path(".")

# Glob for files
audio_files = list(root_dir.glob("*.m4a"))

# Check existence
if json_path.exists():
    # Do something
```

### Shell Command Execution

```python
import subprocess

# Simple command
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

# Quote paths with spaces
cmd = f'ffmpeg -i "{input_file}" -o "{output_file}"'
```

### Environment Variables

```python
from dotenv import load_dotenv
import os

load_dotenv()
HF_TOKEN = os.getenv('HF_TOKEN')
```

---

---

*Last updated: 2026-01-21*
