# AI Workflow Instructions

**For AI**: Read this at every session for daily operations.

**User command**: `Read .2ndBrain/AI-WORKFLOW.md and execute`

## 📋 Prerequisites

**Python Version: 3.9.6 (Required)**

This project requires **Python 3.9.x** specifically (3.9.6 recommended) because:
- WhisperX is unmaintained and optimized for Python 3.9
- Newer Python versions (3.10+) show deprecation warnings
- Python 3.9.6 ensures clean, warning-free operation

**Setup includes automatic Python version checking:**
- `.python-version` file (for pyenv) specifies 3.9.6
- `setup.sh` validates Python version before installation
- Running with wrong Python version will show helpful warnings

**If you don't have Python 3.9.6:**
1. Install pyenv: `brew install pyenv` (macOS)
2. Install Python 3.9.6: `pyenv install 3.9.6`
3. Set for this project: `cd /path/to/2nd-brain && pyenv local 3.9.6`
4. Run setup: `./.2ndBrain/setup.sh`

## 🚀 QUICK START (AI Must Follow)

When user says:
- **"Read .2ndBrain/AI-WORKFLOW.md and execute"**
- **"process"**
- Or similar processing commands

1. **IF audio files exist:** Run `.venv/bin/python3 .2ndBrain/.scripts/transcribe.py` (converts audio → JSON)
2. Run: `.venv/bin/python3 .2ndBrain/.scripts/compile-raw-text.py` (blocks until human types "approved")
3. Create PROCESSING-PLAN.md using semantic search for EVERY item
4. Wait for human approval (or run approval script)
5. Execute all changes from plan
6. **COMPLETE THE WORKFLOW** (see checklist below)

### ✅ AI Completion Checklist (MANDATORY)

After executing changes, AI MUST:
- [ ] Move all processing artifacts to `1-Raw/md/` (RAW-TEXT.md, PROCESSING-PLAN.md, *-ocr.md, Untitled.md)
- [ ] Re-index all modified files: `.venv/bin/python3 .2ndBrain/.scripts/embed-note.py "path/to/file.md"`
- [ ] Verify root is clean (only folders: 1-Raw, 2-Lists, 3-Memos, 4-Wisdom, hidden folders)
- [ ] Report completion with summary of changes

---

## ⚠️ IMPORTANT: Using Virtual Environment Python

**For AI Assistants:** This project uses a virtual environment for dependency isolation. You must ALWAYS use the full venv path when running scripts.

**The venv Python path is:**
```
/Users/mig/Desktop/code/2nd Brain/.venv/bin/python3
```

**Why this matters:**
- Ensures all dependencies (WhisperX, ChromaDB, etc.) are available
- Works reliably across all terminal sessions
- No manual activation needed
- Same behavior for AI and humans

**If venv doesn't exist:**
```bash
cd "/Users/mig/Desktop/code/2nd Brain"
./.2ndBrain/setup.sh
```

📖 **First time setup?** Tell user to run: `Read .2ndBrain/AI-SETUP.md and execute`

---

## Daily Processing ("Read the README.md and process")

**Note:** All commands use full venv path for reliability.

**⚠️ CRITICAL ORDER:** You MUST transcribe audio files BEFORE compiling. The compile script will refuse to run if untranscribed audio exists.

### Step 1A: Transcribe Audio (MUST RUN FIRST if audio files exist)

```bash
cd "/Users/mig/Desktop/code/2nd Brain"
.venv/bin/python3 .2ndBrain/.scripts/transcribe.py
```

**What it does:**
- Transcribes all `.m4a` files at root → JSON files (created in root)
- **Skips files that already have JSON** - safe to run multiple times
- Automatically handles preprocessing (silence removal, 16kHz conversion)
- Automatically handles WhisperX temp_ file naming issue
- **Note:** This step can take a long time for large audio files (roughly 1:1 ratio with diarization)

**When to run:**
- You have new audio files that need transcription
- Skip this if JSON files already exist

**🚨 MANDATORY: This step MUST complete before Step 1B**
- Audio files (.m4a) must be converted to JSON transcripts first
- The compile script will ERROR and exit if untranscribed audio exists
- This ensures all audio content is captured in RAW-TEXT.md

---

### Step 1B: Compile Raw Text (Run AFTER transcription)

```bash
cd "/Users/mig/Desktop/code/2nd Brain"
.venv/bin/python3 .2ndBrain/.scripts/compile-raw-text.py
```

**What it does:**
- **Checks all audio files have been transcribed** (exits with error if not)
- Reads all JSON transcripts from root (with speaker labels)
- Reads all markdown files (.md) at root (excludes system files)
- Runs OCR on images (standalone .jpg/.jpeg/.png & embedded in markdown via `![[image]]`)
- Compiles ALL extracted text → **`RAW-TEXT.md`** (at root for easy review)
- **🛑 HARD-CODED STOP:** Script waits for terminal input - cannot proceed without typing "approved"

**This step is MANDATORY** - it ensures the human reviews raw transcripts before AI processes them.

**⚠️ ERROR HANDLING:**
- If untranscribed audio files exist, script will exit with clear error message
- Run transcribe.py first, then retry compilation

---

### Step 2: Human Reviews RAW-TEXT.md

**CRITICAL: This is now enforced via terminal input requirement.**

1. Review **`RAW-TEXT.md`** at root
2. Fix transcription errors (e.g., "Mizo" → "Mizel", "buy eggs" vs "bought eggs")
3. Correct misspellings, unclear audio, misidentified speakers
4. Check that all important context is captured
5. Edit **`RAW-TEXT.md`** directly
6. **Return to terminal and type "approved"** to continue (or "exit" to stop)

**Why this matters:** AI cannot reliably fix transcription errors. Human review catches:
- Name misspellings (people, places, products)
- Context ambiguities (past vs future tense)
- Technical terms or proper nouns
- Speaker misidentification

**Note:** The script will not continue until you type "approved" in the terminal. This is hard-coded enforcement, not AI instruction.

---

### Step 3: AI Creates PROCESSING-PLAN.md (Using Semantic Search)

**🚨 CRITICAL FOR AI: You MUST use semantic search before recommending actions.**

**Process for AI:**

For EACH item in RAW-TEXT.md:

1. **Identify** what user wants (add/remove/update/create)
2. **Search** using `.venv/bin/python3 .2ndBrain/.scripts/semantic-search.py "relevant query"`
3. **Determine** correct action based on what already exists
4. **Document** recommendation in **`PROCESSING-PLAN.md`** (at root for easy review)

**Example workflow:**

```bash
# User mentions: "Add milk to shopping list"
.venv/bin/python3 .2ndBrain/.scripts/semantic-search.py "shopping list milk"
# → Finds milk already in Shopping.md
# → Recommendation: "No action: Milk already in Shopping.md"

# User mentions: "New app idea for military credit cards"
.venv/bin/python3 .2ndBrain/.scripts/semantic-search.py "app ideas military credit cards"
# → No matches found
# → Recommendation: "Add to 2-Lists/App-Ideas.md: Military credit card optimizer"

# User mentions: "Talked with James about scaling"
.venv/bin/python3 .2ndBrain/.scripts/semantic-search.py "James discussion scaling strategy"
# → Finds 3-Memos/Discussion-with-James.md
# → Recommendation: "Update 3-Memos/Discussion-with-James.md: Add 2026-01-06 scaling discussion"
```

**Recommendation types:**
- **Add to existing list**: "Add to 2-Lists/Shopping.md: Milk"
- **Update existing file**: "Update 3-Memos/Discussion-with-James.md: Add scaling section"
- **Create new file**: "Create 3-Memos/New-Topic.md: [detailed content]"
- **Remove from list**: "Remove from 2-Lists/Tasks.md: Old task XYZ"
- **No action**: "No action: Item already exists in [location]"

**PROCESSING-PLAN.md must acknowledge ALL items from RAW-TEXT.md** - even if recommendation is "No action needed".

---

### Step 4: Human Approves Plan

**CRITICAL: This is now enforced via terminal input requirement.**

**Option A (Recommended): Use approval script**
```bash
.venv/bin/python3 .2ndBrain/.scripts/approve-processing-plan.py
```

**Option B: Manual review**
- Review all recommendations in **`PROCESSING-PLAN.md`** (at root)
- Verify AI didn't miss anything important
- Check that semantic search was used correctly
- Adjust recommendations if needed
- Tell AI: **"approved"** or request modifications

**Why approval script is better:**
- Forces terminal input - AI cannot bypass
- Shows plan summary automatically
- Type "approved" to continue or "reject" to cancel
- Hard-coded enforcement, not AI instruction

**Why this matters:** AI may:
- Miss nuanced context from conversation
- Misinterpret what should go where
- Need guidance on whether to create new files vs update existing

---

### Step 5: AI Executes All Changes

**What AI does:**

1. **Updates lists** in `2-Lists/` (add/remove/modify items)
2. **Creates new memos** in `3-Memos/` as specified in plan
3. **Updates existing memos** with new sections/information
4. **Updates wisdom** in `4-Wisdom/` if applicable
5. **Re-indexes all modified files** for vector database:
   ```bash
   .venv/bin/python3 .2ndBrain/.scripts/embed-note.py "2-Lists/Tasks.md"
   .venv/bin/python3 .2ndBrain/.scripts/embed-note.py "2-Lists/Shopping.md"
   # etc. for each modified file
   ```
6. **Cleans up root folder (MANDATORY):**
   - Moves audio files (.m4a) → `1-Raw/m4a/`
   - Moves JSON files (.json) → `1-Raw/json/`
   - Moves ALL markdown files (.md) INCLUDING Untitled.md → `1-Raw/md/`
   - Moves processing artifacts (RAW-TEXT.md, PROCESSING-PLAN.md, *-ocr.md) → `1-Raw/md/`
   - Removes temporary files (temp_*.wav, etc.)
7. **Verifies root is clean:** Only folders should remain (1-Raw/, 2-Lists/, 3-Memos/, 4-Wisdom/, hidden folders)

**AI MUST complete Steps 5-7 before reporting completion.**

---

### Step 6: Suggest Maintenance (Optional)

After completing workflow, AI can suggest:
- Cleanup of old files in 1-Raw/ if >30 days
- Full re-index if many files changed: `.venv/bin/python3 .2ndBrain/.scripts/init-vector-db.py`

---

## Important Notes for AI

### Hard Stops Are Hard-Coded

The workflow has **mandatory human review points**:

1. **After transcription compilation** - `compile-raw-text.py` exits with clear stop message
2. **After plan creation** - AI must wait for human approval before executing

**Do NOT bypass these stops.** They exist because:
- Transcription errors need human correction
- Strategic decisions need human judgment
- Files should only be moved after verification

### File Naming Edge Case

WhisperX sometimes creates JSON files with `temp_` prefix. Our scripts handle this:
- `transcribe.py` automatically renames `temp_filename.json` → `filename.json`
- If manual transcription needed, always check for and rename temp_ files

### Semantic Search is Mandatory

Before recommending ANY action, AI must:
1. Search for related content: `.venv/bin/python3 .2ndBrain/.scripts/semantic-search.py "query"`
2. Review search results to understand existing structure
3. Make informed recommendation based on what exists

**Never assume** - always search first.

---

## Folder Structure

```
2nd Brain/
├── .venv/                   # Hidden virtual environment (not committed)
├── .chroma/                 # Hidden vector database (not committed)
├── .2ndBrain/               # Hidden system files (committed to Git)
│   ├── .scripts/           # Processing scripts
│   ├── README.md           # This file - main workflow guide
│   ├── SETUP.md            # Detailed setup instructions
│   ├── setup.sh            # Automated setup script
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example        # Environment template
│   └── .gitignore          # Git ignore rules
├── 1-Raw/                   # Organized by file type (not committed)
│   ├── m4a/                # Audio files
│   ├── json/               # Transcription JSONs
│   ├── md/                 # Markdown sources & processing artifacts
│   ├── pdf/                # PDF documents
│   └── jpeg/               # Images
├── 2-Lists/                 # Active working knowledge (your notes)
│   ├── Goals.md
│   ├── Tasks.md
│   ├── Shopping.md
│   ├── App-Ideas.md
│   └── ...
├── 3-Memos/                 # Deep thinking documents (your notes)
│   ├── Discussion-with-James.md
│   └── ...
└── 4-Wisdom/                # Life principles & policies (your notes)
    └── Life-Policies.md
```

**Root directory should be empty** except for:
- Organizational folders above
- Untitled.md (unprocessed capture file)
- Processing artifacts during active session (RAW-TEXT.md, PROCESSING-PLAN.md)

---

## Compression Stages

### Root (L0: 10% Trust)
- Drop zone from phone
- Process immediately, never accumulate
- Files here are temporary during processing

### 1-Raw/ (L1: 30% Trust)
- Organized by file extension for easy management
- Can selectively delete (e.g., just `m4a/` to free space)
- Prompt for cleanup of files >30 days old

### 2-Lists/ (L2: 60% Trust)
- Active working knowledge
- Flat structure, no subfolders
- Examples: `Shopping.md`, `Goals.md`, `Tasks.md`, `App-Ideas.md`
- Compress to memos when validated through action

### 3-Memos/ (L3: 80% Trust)
- Amazon-style 6-pagers
- Deep exploration of ideas
- Connected via [[backlinks]] and #tags
- Compress to wisdom when becomes proven principle

### 4-Wisdom/ (L4: 90% Trust)
- Battle-tested rules
- Life policies and core values
- Operating system for decision-making
- Still re-evaluate, but rarely changes

---

## Compression Examples

**Linear progression:**
Voice recording → `1-Raw/m4a/` → Transcribe to `1-Raw/json/` & `1-Raw/md/` → Extract to `2-Lists/App-Ideas.md` → Test → `3-Memos/analysis.md` → Validates → `4-Wisdom/`

**Skip-level (when immediately impactful):**
Powerful book → `1-Raw/pdf/` → Extract quote → **DIRECTLY** to `4-Wisdom/Life-Policies.md`

**Stays in place (no compression needed):**
"Buy eggs" → `2-Lists/Shopping.md` → Done

---

## Semantic Search (Discovery Layer)

**Find related content across ALL notes by meaning, not just keywords:**

```bash
# Search by topic or concept
.venv/bin/python3 .2ndBrain/.scripts/semantic-search.py "productivity tips"
.venv/bin/python3 .2ndBrain/.scripts/semantic-search.py "morning routines"
.venv/bin/python3 .2ndBrain/.scripts/semantic-search.py "what I learned about habits"

# Results show:
# - File paths with similarity scores
# - Content previews
# - Works even if notes never used exact words
```

**How it works:**
- Every note embedded into vector database (ChromaDB)
- Searches by semantic meaning (AI understands concepts)
- Finds connections you didn't explicitly create
- Complements (doesn't replace) manual [[backlinks]] and #tags

**Use cases:**
- Discovery: "Show everything related to X"
- Cross-reference: Find similar ideas across notes
- Memory: "Where did I write about this?"
- Research: Pull relevant content for new memo
- **Planning: Check what exists before adding new content**

---

## Common Commands

```bash
# All commands run from project root: /Users/mig/Desktop/code/2nd Brain

# Full processing workflow (IN THIS ORDER)
.venv/bin/python3 .2ndBrain/.scripts/transcribe.py              # Step 1A: MUST RUN FIRST if audio exists
.venv/bin/python3 .2ndBrain/.scripts/compile-raw-text.py        # Step 1B: Run after transcription
# → Review RAW-TEXT.md, tell AI "approved"
# → AI creates PROCESSING-PLAN.md using semantic search
# → Review PROCESSING-PLAN.md, tell AI "approved"
# → AI executes all changes and cleans up

# Individual operations
.venv/bin/python3 .2ndBrain/.scripts/semantic-search.py "query" # Search by meaning
.venv/bin/python3 .2ndBrain/.scripts/embed-note.py "file.md"    # Re-index single file
.venv/bin/python3 .2ndBrain/.scripts/init-vector-db.py          # Re-index everything

# Check system
.venv/bin/python3 -m whisperx --version            # Verify WhisperX installed
ls -la                                            # List root files
find 1-Raw -type f -mtime +30                     # Find old files for cleanup
```

---

## Debugging Common Issues

### Transcription

**Issue:** JSON not found after transcription
- **Check:** Look for `temp_filename.json` in root
- **Fix:** Rename to `filename.json` manually
- **Prevention:** Use `transcribe.py` which handles this automatically

**Issue:** Transcription too slow
- **Normal:** Diarization runs at roughly 1:1 ratio (3 hour audio = 3 hour processing)
- **Help:** Script preprocessing removes silence, can save 20-40%
- **Alternative:** Run overnight

### RAW-TEXT.md

**Issue:** Transcription has errors
- **Expected:** AI transcription isn't perfect
- **Fix:** Edit RAW-TEXT.md directly before approving
- **Common:** Names, technical terms, past/future tense

### PROCESSING-PLAN.md

**Issue:** AI didn't use semantic search
- **Check:** Look for search results in AI's working
- **Fix:** Explicitly ask AI to search first
- **Remind:** "Use semantic search to check existing content"

---

## Brainstorming Questions

- "What should I do next?" → `2-Lists/Goals.md`
- "What's my philosophy on X?" → `4-Wisdom/`
- "What did I capture recently?" → `1-Raw/md/`
- "What article ideas do I have?" → `2-Lists/Article-Ideas.md`
- "Find notes about productivity" → Search `#productivity` or `[[Productivity]]`
- "Find everything about X" → `.venv/bin/python3 .2ndBrain/.scripts/semantic-search.py "X"`

---

**Remember**: 
- Compression stops when useful, jumps when validated
- This is a living system - update this workflow as you learn
- Hard stops exist for good reason - don't bypass them
- Semantic search is mandatory before planning
- Human review catches what AI cannot

**Vibe Coding in Obsidian**: Everything is Markdown-visible for AI assistants.

*Last updated: 2026-01-06*
