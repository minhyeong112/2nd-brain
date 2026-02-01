# Cloud LLM Instance - Second Brain

## You Are Here

Working directory: `/Users/mig/Desktop/code/2nd Brain/Cloud-LLM-Access/`

You are the **Cloud LLM instance** (Claude) with full access to all Second Brain tools and content.

## What You Have Access To

**Everything you need is in this directory:**
- `.2ndBrain/` - Framework scripts, workflows, setup docs
- `.venv/` - Python environment
- `.chroma/` - Vector database for semantic search
- `Lists/`, `Tasks/`, `Memos/`, `Conversations/`, `Wisdom/`, `Shopping/`, `Contacts/` - User content

## What You CANNOT Access

**The parent directory (`../`) contains sensitive content:**
- Personal journals
- Private notes
- Substance use references  
- Deeply personal thoughts

**DO NOT attempt to access parent directory:**
- ❌ No `ls ../` or `cd ..`
- ❌ No `/Users/mig/Desktop/code/2nd\ Brain/` absolute paths
- ❌ If you need parent access, tell user you don't have it

**Privacy screening happens BEFORE content reaches you.** Trust that sensitive content has already been filtered out.

---

## Commands

### Process files
When user says "process":
1. Read `.2ndBrain/AI-WORKFLOW.md`
2. Execute workflow (file-by-file processing, NOT bulk)

### Setup
When user says "setup":
- Read and execute `.2ndBrain/AI-SETUP.md`

### Semantic search
Before recommending actions:
```bash
.venv/bin/python3 .2ndBrain/skills/semantic-search.py "query"
```

---

## Python Environment

**Always use venv Python:**
```bash
.venv/bin/python3 <script>
```

## File Discovery

**Always use `ls` to list files, not glob patterns:**
```bash
ls -la Tasks/        # List directory contents
ls -la Tasks/*.md    # List specific types
```

Glob patterns can fail even when files exist.

---

## Processing Workflow (File-by-File)

When user says "process":

1. **Scan for unprocessed files** in this directory root (not in subfolders)
2. **Process ONE file at a time** (NOT bulk):
   - Transcribe audio if needed (`.m4a` files)
   - Generate PROCESSING-PLAN.md for THIS FILE ONLY
   - Present plan to user
   - Wait for approval
   - Execute plan
   - Move to next file
3. **Never create RAW-TEXT.md** - File-by-file prevents context window explosion
4. **Semantic indexing** after processing each file

## What NOT to Process

- `AGENTS.md` - System file
- `CLAUDE.md` - This file
- `.2ndBrain/` - Framework code
- Files already organized in subfolders (unless user asks)

---

## Organization Rules

- **One layer deep** - No sub-lists within files, create separate files instead
  - ✅ `Tasks-Urgent.md`, `Tasks-Admin.md`, `Tasks-Health.md`
  - ❌ One `Tasks.md` with nested categories
- **File naming:**
  - Notes: `Title-Case.md`
  - Categories: `Category-Subcategory.md`
  - Scripts: `kebab-case.py`
- **Hard stops** - Always get user approval before executing plans

## Mandatory Semantic Search

Before recommending where to place content:
```bash
.venv/bin/python3 .2ndBrain/skills/semantic-search.py "query"
```

---

## Code Style

### Python
- 4 spaces, max 120 chars
- Double quotes for strings
- Type hints optional
- Docstrings for public functions

### Error Handling
- Descriptive errors with emoji (❌, ⚠️, ✅)
- Exit code 1 on failure, 0 on success
- Fail fast with clear messages

### File Operations
- Use `Path` from pathlib
- Quote paths with spaces in shell commands
- Use context managers for I/O

---

## Security

- Never commit `.env` (contains API keys)
- Never commit personal notes
- Never log API tokens
- Never commit `.chroma/` database
- Never access parent directory

---

## Detailed Documentation

- `.2ndBrain/AI-WORKFLOW.md` - Full processing workflow
- `.2ndBrain/AI-SETUP.md` - Setup instructions
- `AGENTS.md` - Quick reference (points to this file)

---

*Last updated: 2026-02-01*
