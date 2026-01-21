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

1. **IF audio files exist:** Run `.venv/bin/python3 .2ndBrain/skills/transcribe.py` (converts audio → JSON)
2. Run: `.venv/bin/python3 .2ndBrain/skills/compile-raw-text.py` (blocks until human types "approved")
3. Create PROCESSING-PLAN.md using semantic search for EVERY item
4. Wait for human approval (or run approval script)
5. Execute all changes from plan
6. **COMPLETE THE WORKFLOW** (see checklist below)

### ✅ AI Completion Checklist (MANDATORY)

After executing changes, AI MUST:
- [ ] Move all processing artifacts to `.Archive/md/` (RAW-TEXT.md, PROCESSING-PLAN.md, *-ocr.md, Untitled.md)
- [ ] Re-index all modified files: `.venv/bin/python3 .2ndBrain/skills/embed-note.py "path/to/file.md"`
- [ ] Verify root is clean (only folders: .Archive, Lists, Memos, Wisdom, Conversations, Tasks, hidden folders)
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
.venv/bin/python3 .2ndBrain/skills/transcribe.py
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
.venv/bin/python3 .2ndBrain/skills/compile-raw-text.py
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
2. **Search** using `.venv/bin/python3 .2ndBrain/skills/semantic-search.py "relevant query"`
3. **Determine** correct action based on what already exists
4. **Document** recommendation in **`PROCESSING-PLAN.md`** (at root for easy review)

**Example workflow:**

```bash
# User mentions: "Add milk to shopping list"
.venv/bin/python3 .2ndBrain/skills/semantic-search.py "shopping list milk"
# → Finds milk already in Shopping.md
# → Recommendation: "No action: Milk already in Shopping.md"

# User mentions: "New app idea for military credit cards"
.venv/bin/python3 .2ndBrain/skills/semantic-search.py "app ideas military credit cards"
# → No matches found
# → Recommendation: "Add to Lists/App-Ideas.md: Military credit card optimizer"

# User mentions: "Talked with James about scaling"
.venv/bin/python3 .2ndBrain/skills/semantic-search.py "James discussion scaling strategy"
# → Finds Conversations/Discussion-with-James.md
# → Recommendation: "Update Conversations/Discussion-with-James.md: Add 2026-01-06 scaling discussion"
```

**Recommendation types:**
- **Add to existing list**: "Add to Lists/Shopping.md: Milk"
- **Update existing file**: "Update Conversations/Discussion-with-James.md: Add scaling section"
- **Create new file**: "Create Memos/New-Topic.md: [detailed content]"
- **Remove from list**: "Remove from Tasks/Tasks.md: Old task XYZ"
- **No action**: "No action: Item already exists in [location]"

**PROCESSING-PLAN.md must acknowledge ALL items from RAW-TEXT.md** - even if recommendation is "No action needed".

---

### Step 4: Human Approves Plan

**CRITICAL: This is now enforced via terminal input requirement.**

**Option A (Recommended): Use approval script**
```bash
.venv/bin/python3 .2ndBrain/skills/approve-processing-plan.py
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

1. **Updates lists** in `Lists/` (add/remove/modify items)
2. **Updates tasks** in `Tasks/` by category (Tasks-Urgent.md, Tasks-Admin.md, etc.)
3. **Updates shopping** in `Shopping/` by category (Shopping-Groceries.md, Shopping-Miami.md, etc.)
4. **Updates contacts** in `Contacts/` by category (Contacts-Healthcare.md, Contacts-Korea.md, etc.)
5. **Creates new memos** in `Memos/` as specified in plan
6. **Updates existing conversations** in `Conversations/` with new sections/information
7. **Updates wisdom** in `Wisdom/` if applicable
8. **Re-indexes all modified files** for vector database:
   ```bash
   .venv/bin/python3 .2ndBrain/skills/embed-note.py "Tasks/Tasks-Urgent.md"
   .venv/bin/python3 .2ndBrain/skills/embed-note.py "Shopping/Shopping-Groceries.md"
   # etc. for each modified file
   ```
9. **Cleans up root folder (MANDATORY):**
   - Moves audio files (.m4a) → `.Archive/m4a/`
   - Moves JSON files (.json) → `.Archive/json/`
   - Moves ALL markdown files (.md) INCLUDING Untitled.md → `.Archive/md/`
   - Moves processing artifacts (RAW-TEXT.md, PROCESSING-PLAN.md, *-ocr.md) → `.Archive/md/`
   - Removes temporary files (temp_*.wav, etc.)
10. **Verifies root is clean:** Only folders should remain (.Archive/, Lists/, Memos/, Wisdom/, Conversations/, Tasks/, Shopping/, Contacts/, hidden folders)

**AI MUST complete Steps 5-10 before reporting completion.**

**When adding items to categorized folders (Tasks/Shopping/Contacts)**:
- Use semantic search to find existing category files
- Add to existing file if appropriate category exists
- Create new category file if no existing category fits
- Never create sublists or subheadings within a file

---

### Step 6: Suggest Maintenance (Optional)

After completing workflow, AI can suggest:
- Cleanup of old files in .Archive/ if >30 days
- Full re-index if many files changed: `.venv/bin/python3 .2ndBrain/skills/init-vector-db.py`

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
1. Search for related content: `.venv/bin/python3 .2ndBrain/skills/semantic-search.py "query"`
2. Review search results to understand existing structure
3. Make informed recommendation based on what exists

**Never assume** - always search first.

---

## Folder Structure

```
2nd Brain/
├── .venv/                   # Hidden virtual environment (not committed)
├── .chroma/                 # Hidden vector database (not committed)
├── .Archive/                # Historical source files (not committed)
│   ├── m4a/                # Audio files
│   ├── json/               # Transcription JSONs
│   ├── md/                 # Markdown sources & processing artifacts
│   ├── pdf/                # PDF documents
│   └── jpeg/               # Images
├── .2ndBrain/               # Second Brain system (committed to Git)
│   ├── skills/             # Python skills (transcribe, search, embed, etc.)
│   ├── AI-WORKFLOW.md      # This file - main workflow guide
│   ├── AI-SETUP.md         # Initial setup guide
│   ├── setup.sh            # Automated setup script
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment template
├── Lists/                   # Active working knowledge (your notes)
│   ├── Goals.md
│   ├── App-Ideas.md
│   └── ...
├── Memos/                   # Deep thinking documents (your notes)
│   ├── AI-Safety-Alignment-Ideas.md
│   └── ...
├── Wisdom/                  # Life principles & policies (your notes)
│   └── Life-Policies.md
├── Conversations/           # Discussion notes (your notes)
│   ├── Discussion-with-James.md
│   └── ...
├── Tasks/                   # Task management by category (your notes)
│   ├── Tasks-Urgent.md
│   ├── Tasks-Admin.md
│   ├── Tasks-Health.md
│   └── ...
├── Shopping/                # Shopping lists by category (your notes)
│   ├── Shopping-Groceries.md
│   ├── Shopping-Miami.md
│   ├── Shopping-Electronics-Tech.md
│   └── ...
└── Contacts/                # Contact lists by category (your notes)
    ├── Contacts-Healthcare.md
    ├── Contacts-Korea.md
    ├── Contacts-Business-Professional.md
    └── ...
```

**Root directory should be empty** except for:
- Organizational folders above
- Untitled.md (unprocessed capture file)
- Processing artifacts during active session (RAW-TEXT.md, PROCESSING-PLAN.md)

**Naming Convention for Categorized Files**:
- Tasks: `Tasks-[Category].md` (e.g., Tasks-Urgent, Tasks-Admin, Tasks-Health)
- Shopping: `Shopping-[Category].md` (e.g., Shopping-Groceries, Shopping-Miami)
- Contacts: `Contacts-[Category].md` (e.g., Contacts-Healthcare, Contacts-Korea)

**One Layer Deep Principle**: No sublists or subheadings within files. Create separate category files instead.

---

## Compression Stages

### Root (L0: 10% Trust)
- Drop zone from phone
- Process immediately, never accumulate
- Files here are temporary during processing

### .Archive/ (L1: 30% Trust)
- Organized by file extension for easy management
- Can selectively delete (e.g., just `m4a/` to free space)
- Prompt for cleanup of files >30 days old

### Lists/ (L2: 60% Trust)
- Active working knowledge
- Flat structure, no subfolders
- Examples: `Shopping.md`, `Goals.md`, `App-Ideas.md`
- Compress to memos when validated through action

### Tasks/ (L2: 60% Trust)
- Task management by category
- Separate from general lists for focus
- Examples: `Tasks-Urgent.md`, `Tasks-Admin.md`, `Tasks-Health.md`
- Compress to memos when task becomes insight

### Shopping/ (L2: 60% Trust)
- Shopping lists by category
- Examples: `Shopping-Groceries.md`, `Shopping-Miami.md`, `Shopping-Electronics-Tech.md`
- Archive completed purchases or consolidate when needed

### Contacts/ (L2: 60% Trust)
- Contact lists by category
- Examples: `Contacts-Healthcare.md`, `Contacts-Korea.md`, `Contacts-Business-Professional.md`
- Update as relationships and contact info change

### Memos/ (L3: 80% Trust)
- Amazon-style 6-pagers
- Deep exploration of ideas
- Connected via [[backlinks]] and #tags
- Compress to wisdom when becomes proven principle

### Conversations/ (L3: 80% Trust)
- Discussion notes and meeting summaries
- Track important conversations over time
- Extract insights to move to Memos or Wisdom

### Wisdom/ (L4: 90% Trust)
- Battle-tested rules
- Life policies and core values
- Operating system for decision-making
- Still re-evaluate, but rarely changes

---

## Compression Examples

**Linear progression:**
Voice recording → `.Archive/m4a/` → Transcribe to `.Archive/json/` & `.Archive/md/` → Extract to `Lists/App-Ideas.md` → Test → `Memos/analysis.md` → Validates → `Wisdom/`

**Skip-level (when immediately impactful):**
Powerful book → `.Archive/pdf/` → Extract quote → **DIRECTLY** to `Wisdom/Life-Policies.md`

**Stays in place (no compression needed):**
"Buy eggs" → `Lists/Shopping.md` → Done

---

## Semantic Search (Discovery Layer)

**Find related content across ALL notes by meaning, not just keywords:**

```bash
# Search by topic or concept
.venv/bin/python3 .2ndBrain/skills/semantic-search.py "productivity tips"
.venv/bin/python3 .2ndBrain/skills/semantic-search.py "morning routines"
.venv/bin/python3 .2ndBrain/skills/semantic-search.py "what I learned about habits"

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
.venv/bin/python3 .2ndBrain/skills/transcribe.py              # Step 1A: MUST RUN FIRST if audio exists
.venv/bin/python3 .2ndBrain/skills/compile-raw-text.py        # Step 1B: Run after transcription
# → Review RAW-TEXT.md, tell AI "approved"
# → AI creates PROCESSING-PLAN.md using semantic search
# → Review PROCESSING-PLAN.md, tell AI "approved"
# → AI executes all changes and cleans up

# Individual operations
.venv/bin/python3 .2ndBrain/skills/semantic-search.py "query" # Search by meaning
.venv/bin/python3 .2ndBrain/skills/embed-note.py "file.md"    # Re-index single file
.venv/bin/python3 .2ndBrain/skills/init-vector-db.py          # Re-index everything

# Check system
.venv/bin/python3 -m whisperx --version            # Verify WhisperX installed
ls -la                                            # List root files
find .Archive -type f -mtime +30                  # Find old files for cleanup
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

- "What should I do next?" → `Lists/Goals.md` or `Tasks/`
- "What's my philosophy on X?" → `Wisdom/`
- "What did I capture recently?" → `.Archive/md/`
- "What article ideas do I have?" → `Lists/Article-Ideas.md`
- "Who did I talk to about X?" → `Conversations/`
- "Find notes about productivity" → Search `#productivity` or `[[Productivity]]`
- "Find everything about X" → `.venv/bin/python3 .2ndBrain/skills/semantic-search.py "X"`

---

**Remember**: 
- Compression stops when useful, jumps when validated
- This is a living system - update this workflow as you learn
- Hard stops exist for good reason - don't bypass them
- Semantic search is mandatory before planning
- Human review catches what AI cannot

**Vibe Coding in Obsidian**: Everything is Markdown-visible for AI assistants.

*Last updated: 2026-01-06*
