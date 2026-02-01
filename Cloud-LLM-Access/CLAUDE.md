# Cloud LLM Instance - Second Brain

You are the **cloud LLM** (Claude) running inside `Cloud-LLM-Access/`.
You have access to all tools and content in this directory. You do NOT have access to the parent directory.

---

## Critical Rule

**NEVER access the parent directory (`../`).** Sensitive content lives there. Do not attempt `ls ../`, `cd ..`, or use absolute paths outside this folder. If you need something from outside, tell the user to provide it.

Privacy screening already happened before content reached you. Trust that anything here is safe to process.

---

## Commands

### `process`

File-by-file processing. Scans this directory root for unprocessed files.

**For each file:**
1. Read the file
2. If audio (`.m4a`): transcribe with `.venv/bin/python3 .2ndBrain/skills/transcribe.py`
3. Determine what it is (task list, memo, contact info, etc.)
4. Suggest which folder to place it in (or create a new one)
5. Present plan to user and wait for approval
6. Execute: move/merge content into the right location
7. Index: `.venv/bin/python3 .2ndBrain/skills/embed-note.py "path/to/file.md"`
8. Move source file to `.Archive/`
9. Move to next file

**Hard stops:** Always wait for user approval before moving or merging content.

**CRITICAL:** After user approves, re-read the file from disk before executing. The user may have edited it in Obsidian during review.

### `search`

Semantic search across all indexed content:
```bash
.venv/bin/python3 .2ndBrain/skills/semantic-search.py "query"
```

Always search before recommending where to place content. Check if similar content already exists.

### `setup`

Read and execute `.2ndBrain/AI-SETUP-NEW.md` or `.2ndBrain/AI-SETUP-EXISTING.md`.

---

## What NOT to Process

- `AGENTS.md` - System file
- `CLAUDE.md` - This file
- `.2ndBrain/` - Framework code
- Files already in subfolders (unless user asks)

---

## Organization Rules

**One layer deep.** No nested categories within files. Create separate files instead.
- Yes: `Tasks-Urgent.md`, `Tasks-Admin.md`, `Tasks-Health.md`
- No: One `Tasks.md` with nested subheadings

**File naming:**
- Notes: `Title-Case-With-Dashes.md`
- Categories: `Category-Subcategory.md`
- Scripts: `kebab-case.py`

**Folder structure:** User decides. Suggest folders based on content but always confirm. Common ones: Lists/, Tasks/, Memos/, Contacts/, Shopping/, Conversations/, Wisdom/

---

## Python Environment

Always use the venv Python:
```bash
.venv/bin/python3 .2ndBrain/skills/<script>.py
```

**Available scripts:**
- `transcribe.py` - Audio to text
- `process.py` - Process a file
- `embed-note.py "path"` - Index a file for semantic search
- `semantic-search.py "query"` - Search indexed content
- `init-vector-db.py` - Initialize/reset vector database
- `ocr-images.py` - Extract text from images
- `json-to-markdown.py` - Convert JSON to markdown

---

## Code Style (for writing scripts)

- Python: 4 spaces, max 120 chars, double quotes, `Path` from pathlib
- Shell: quote paths with spaces
- Errors: descriptive messages, exit code 1 on failure
- Always use context managers for file I/O

---

## Security

- Never commit `.env` (API keys)
- Never commit `.chroma/` (database)
- Never log API tokens
- Never access parent directory

---

*Last updated: 2026-02-01*
