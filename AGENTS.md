# AI Agent Guidelines

## Commands

### Process files
When user says "process" or similar:
1. Read `.2ndBrain/AI-WORKFLOW.md`
2. Execute complete workflow

### Setup
When user says "setup":
- Read and execute `.2ndBrain/AI-SETUP.md`

## Python Environment

**Always use venv Python:**
```bash
.venv/bin/python3 <script>
```

## File Discovery

**CRITICAL: Always use `ls` to list files, not glob patterns:**
```bash
ls -la Tasks/        # List directory contents
ls -la Tasks/*.md    # List specific types
```

Glob patterns can fail even when files exist. Use `ls` first, then read files.

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

## Repository Structure

```
2nd Brain/
├── .2ndBrain/        # System (committed)
├── .venv/            # Python env (gitignored)
├── .chroma/          # Vector DB (gitignored)
├── .Archive/         # Source files (gitignored)
├── Lists/            # Working knowledge (gitignored)
├── Memos/            # Deep thinking (gitignored)
├── Wisdom/           # Principles (gitignored)
├── Conversations/    # Discussion notes (gitignored)
├── Tasks/            # By category (gitignored)
├── Shopping/         # By category (gitignored)
├── Contacts/         # By category (gitignored)
└── AGENTS.md         # This file (committed)
```

## Organization: One Layer Deep

**No subheadings or sublists in files.** Create separate files instead.

**Examples:**
- ❌ Tasks.md with nested categories
- ✅ Tasks-Urgent.md, Tasks-Admin.md, Tasks-Health.md

## Workflow Rules

### Mandatory Semantic Search
Before recommending actions, search:
```bash
.venv/bin/python3 .2ndBrain/skills/semantic-search.py "query"
```

### Processing Order (Strict)
1. Transcribe audio (if .m4a files exist)
2. Compile raw text → RAW-TEXT.md
3. **Human approval required**
4. Create PROCESSING-PLAN.md (using semantic search)
5. **Human approval required**
6. Execute changes
7. Re-index modified files
8. Clean up root folder

### Hard Stops
- After RAW-TEXT.md: Human reviews/fixes transcription errors
- After PROCESSING-PLAN.md: Human approves plan

### File Cleanup
Move to `.Archive/`:
- Audio (.m4a) → `m4a/`
- JSON (.json) → `json/`
- Markdown (.md) → `md/`
- Delete temp files

Root should only have folders after processing.

## Naming Conventions

**Files:**
- Scripts: `kebab-case.py`
- Notes: `Title-Case.md`
- Processing: `UPPERCASE.md`
- Categories: `Category-Subcategory.md`

**Variables:**
- Python: `snake_case`
- Constants: `UPPER_SNAKE_CASE`

## Security

- Never commit `.env` (contains HF_TOKEN)
- Never commit personal notes
- Never log API tokens
- Never commit `.chroma/` database

---

*Last updated: 2026-01-21*
