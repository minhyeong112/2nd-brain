# AI Workflow - Organize

**For AI:** Read this when user says "organize".

---

## Workflow

1. **Scan** for `.md` files in this directory root (not subfolders)
2. **Skip:** `AGENTS.md`, `CLAUDE.md`, anything in `.2ndBrain/`
3. **For each file:**
   a. Read the file
   b. Summarize what it contains (tasks, contacts, memo, ideas, etc.)
   c. Search for related content: `.venv/bin/python3 .2ndBrain/skills/semantic-search.py "query"`
   d. Make a plan: which folder, merge with existing file or create new
   e. **STOP. Present plan to user. Wait for "approved".**
   f. **Re-read file from disk** (user may have edited during review)
   g. Execute: create/edit files in destination folder
   h. Index: `.venv/bin/python3 .2ndBrain/skills/embed-note.py "path/to/file.md"`
   i. Copy original to `.Archive/`, delete from root
4. **Repeat** for next file
5. **Done:** "Organization complete. X files processed."

## Hard Stop

After step (e): user reviews the plan. They may edit the file in Obsidian before approving.

**CRITICAL:** After approval, re-read the file from disk. Any previously cached content is stale.

## Rules

- **One file at a time.** Never batch.
- **Search before placing.** Always check if similar content exists.
- **User decides folder structure.** Suggest, don't impose.
- **One layer deep.** No nested categories. Separate files instead.
- **Always use venv:** `.venv/bin/python3`
- **Archive originals.** Copy to `.Archive/` before removing from root.

## Available Scripts

```bash
.venv/bin/python3 .2ndBrain/skills/semantic-search.py "q"  # Search
.venv/bin/python3 .2ndBrain/skills/embed-note.py "path"    # Index
.venv/bin/python3 .2ndBrain/skills/json-to-markdown.py     # JSON → md
```

---

*Last updated: 2026-02-01*
