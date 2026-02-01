# Cloud LLM Instance - Second Brain

You are the **cloud LLM** (Claude) running inside `Cloud-LLM-Access/`.
You have access to all tools and content in this directory. You do NOT have access to the parent directory.

---

## Critical Rule

**NEVER access the parent directory (`../`).** Sensitive content lives there. Do not attempt `ls ../`, `cd ..`, or use absolute paths outside this folder. If you need something from outside, tell the user to provide it.

Privacy screening and transcription already happened before content reached you. Everything here is safe to process.

---

## Commands

### `process`

File-by-file processing. Scans this directory root for unprocessed `.md` files.

**For each file:**
1. Read the file
2. Determine what it is (task list, memo, contact info, etc.)
3. Search for related content: `.venv/bin/python3 .2ndBrain/skills/semantic-search.py "query"`
4. Suggest which folder to place it in (or create a new one)
5. Present plan to user and **wait for approval**
6. **Re-read file from disk** (user may have edited in Obsidian)
7. Execute: move/merge content into the right location
8. Index: `.venv/bin/python3 .2ndBrain/skills/embed-note.py "path/to/file.md"`
9. Move source file to `.Archive/`
10. Move to next file

**Hard stops:** Always wait for user approval before moving or merging content.

### `search`

Semantic search across all indexed content:
```bash
.venv/bin/python3 .2ndBrain/skills/semantic-search.py "query"
```

Always search before recommending where to place content.

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

**File naming:** `Title-Case-With-Dashes.md`

**Folder structure:** User decides. Suggest based on content, always confirm.

---

## Python Environment

Always use the venv:
```bash
.venv/bin/python3 .2ndBrain/skills/<script>.py
```

**Available scripts:**
- `semantic-search.py "query"` - Search indexed content
- `embed-note.py "path"` - Index a file
- `init-vector-db.py` - Initialize/reset vector database
- `json-to-markdown.py` - Convert JSON to markdown
- `process.py` - Process a file

---

## Security

- Never access parent directory
- Never commit `.env` or `.chroma/`
- Never log API tokens

---

*Last updated: 2026-02-01*
