# AI Workflow

**For AI**: Read this at every session for daily operations.

## Quick Start

When user says "process":

1. **IF audio exists:** `.venv/bin/python3 .2ndBrain/skills/transcribe.py`
2. **Compile:** `.venv/bin/python3 .2ndBrain/skills/compile-raw-text.py` (waits for "approved")
3. **Plan:** **Re-read RAW-TEXT.md from disk** (human may have edited it!), then create PROCESSING-PLAN.md using semantic search for EVERY item
4. **Wait:** Human types "approved"
5. **Execute:** **Re-read PROCESSING-PLAN.md from disk** (human may have edited it!), then execute all changes from plan
6. **Cleanup:** 
   - Re-index: `.venv/bin/python3 .2ndBrain/skills/embed-note.py "path"`
   - Move files to `.Archive/`
   - Verify root is clean (folders only)

## Hard Stops

1. After Step 2: Human reviews RAW-TEXT.md, fixes errors, types "approved"
2. After Step 3: Human reviews plan, types "approved"

**CRITICAL: After EVERY hard stop, the AI MUST re-read the file from disk before proceeding.**
The human edits files in Obsidian during review. Any previously cached/read content is stale.
- After RAW-TEXT.md approval → Re-read RAW-TEXT.md, THEN create processing plan
- After PROCESSING-PLAN.md approval → Re-read PROCESSING-PLAN.md, THEN execute

## Semantic Search (Mandatory)

Before ANY recommendation:
```bash
.venv/bin/python3 .2ndBrain/skills/semantic-search.py "query"
```

Example workflow:
```bash
# User: "Add milk to shopping"
.venv/bin/python3 .2ndBrain/skills/semantic-search.py "shopping milk"
# → Check if exists before adding
```

## Processing Order (Strict)

1. Transcribe audio → JSON
2. Compile → RAW-TEXT.md
3. Human approval → "approved"
4. Create plan with search
5. Human approval → "approved"
6. Execute changes
7. Re-index modified files
8. Clean root (move to .Archive/)

## File Structure

```
Root (temp only during processing)
├── .Archive/           # Historical (m4a/, json/, md/, pdf/, jpeg/)
├── Lists/              # Active knowledge
├── Tasks/              # By category (Tasks-Urgent.md, etc.)
├── Shopping/           # By category (Shopping-Groceries.md, etc.)
├── Contacts/           # By category (Contacts-Healthcare.md, etc.)
├── Memos/              # Deep thinking
├── Conversations/      # Discussion notes
└── Wisdom/             # Principles
```

## One Layer Deep

No subheadings or sublists. Create separate files instead.

## Compression Stages

- **Root:** Process immediately, never accumulate
- **.Archive/:** Historical sources (30% trust)
- **Lists/Tasks/Shopping/Contacts:** Active (60% trust)
- **Memos/Conversations:** Deep thinking (80% trust)
- **Wisdom/:** Battle-tested (90% trust)

## Common Commands

```bash
# Process workflow
.venv/bin/python3 .2ndBrain/skills/transcribe.py
.venv/bin/python3 .2ndBrain/skills/compile-raw-text.py

# Search & index
.venv/bin/python3 .2ndBrain/skills/semantic-search.py "query"
.venv/bin/python3 .2ndBrain/skills/embed-note.py "file.md"
.venv/bin/python3 .2ndBrain/skills/init-vector-db.py
```

## Key Rules

- Always use venv Python: `.venv/bin/python3`
- Search before recommending
- Wait for human approval at hard stops
- **ALWAYS re-read files from disk after a hard stop before proceeding (human edits during review!)**
- Clean root after processing
- Re-index modified files

---

*Last updated: 2026-01-21*
