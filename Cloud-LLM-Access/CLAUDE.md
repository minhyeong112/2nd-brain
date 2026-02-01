# Cloud LLM Instance - Second Brain

You are the **cloud LLM** (Claude) running inside `Cloud-LLM-Access/`.
Everything you need is in this directory. You do NOT have access to the parent directory.

---

## Critical Rule

**NEVER access the parent directory (`../`).** Sensitive content lives there. Do not attempt `ls ../`, `cd ..`, or use absolute paths outside this folder. If you need something from outside, tell the user to provide it.

All content here has already been privacy-screened and redacted. It is safe to process.

---

## Commands

### `organize`

File-by-file organization. Scans this directory root for unprocessed `.md` files.

**Before starting:** Create `.Archive/` folder if it doesn't exist: `mkdir -p .Archive`

**For each file:**
1. Read the file
2. Summarize what it contains
3. Search for related content: `.venv/bin/python3 .2ndBrain/skills/semantic-search.py "query"`
4. Make a plan: suggest which folder to place it in, whether to merge with an existing file or create a new one
5. **Present plan to user. Wait for approval.**
6. **Re-read file from disk** (user may have edited in Obsidian during review)
7. Execute the plan: create/edit files in the destination folder
8. Index: `.venv/bin/python3 .2ndBrain/skills/embed-note.py "path/to/file.md"`
9. Copy the original source file to `.Archive/`
10. Delete the source file from root
11. Move to next file

**Hard stop:** Always wait for user approval (step 5) before executing. After approval, always re-read from disk - the user may have edited the file.

**What NOT to process:**
- `AGENTS.md`, `CLAUDE.md` - System files
- `.2ndBrain/` - Framework code
- Files already in subfolders (unless user asks)

### `search`

Semantic search across indexed content:
```bash
.venv/bin/python3 .2ndBrain/skills/semantic-search.py "query"
```

Always search before recommending where to place content.

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
- `embed-note.py "path"` - Index a file for semantic search
- `init-vector-db.py` - Initialize/reset vector database
- `json-to-markdown.py` - Convert JSON to markdown

---

## Folder Structure

```
Cloud-LLM-Access/        ← You are here
├── .2ndBrain/            ← Framework (scripts, docs)
├── .Archive/             ← Originals of organized files
├── .chroma/              ← Vector database
├── .venv/                ← Python environment
├── .env                  ← API keys
├── AGENTS.md             ← Points to this file
├── CLAUDE.md             ← This file
├── (unprocessed files)   ← Land here from ingest, organize them
└── (user folders)/       ← Organized content (Lists/, Tasks/, etc.)
```

## Security

- Never access parent directory
- Never commit `.env` or `.chroma/`
- Never log API tokens

---

*Last updated: 2026-02-01*
