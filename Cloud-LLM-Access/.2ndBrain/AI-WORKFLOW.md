# AI Workflow - File-by-File Processing

**For AI:** Read this when user says "process".

---

## Workflow

1. **Scan** for unprocessed files in this directory root (not subfolders)
2. **For each file:**
   a. Read the file contents
   b. If `.m4a`: `.venv/bin/python3 .2ndBrain/skills/transcribe.py`
   c. Summarize what the file contains
   d. Search for related content: `.venv/bin/python3 .2ndBrain/skills/semantic-search.py "query"`
   e. Suggest destination folder and whether to merge with existing file or create new
   f. **STOP.** Present plan to user. Wait for approval.
   g. **Re-read file from disk** (user may have edited during review)
   h. Execute: move/merge content
   i. Index: `.venv/bin/python3 .2ndBrain/skills/embed-note.py "path/to/file.md"`
   j. Move source to `.Archive/`
3. **Repeat** for next file
4. **Done:** "Processing complete. X files processed."

## Hard Stops

- After step (f): User reviews the plan, may edit the file, then says "approved"
- **CRITICAL:** After every approval, re-read the file from disk before proceeding. The user edits in Obsidian during review. Any cached content is stale.

## Rules

- **One file at a time.** Never batch process.
- **Search before placing.** Always check if similar content exists.
- **Never create RAW-TEXT.md.** That's the old workflow. File-by-file prevents context explosion.
- **User decides folder structure.** Suggest, don't impose.
- **One layer deep.** No nested categories. Create separate files instead.
- **Always use venv:** `.venv/bin/python3`
- **Clean root after processing.** Only folders should remain.

## What NOT to Process

- `AGENTS.md`, `CLAUDE.md` - System files
- `.2ndBrain/` - Framework
- Files already in subfolders

## Available Scripts

```bash
.venv/bin/python3 .2ndBrain/skills/transcribe.py          # Audio → text
.venv/bin/python3 .2ndBrain/skills/semantic-search.py "q"  # Search
.venv/bin/python3 .2ndBrain/skills/embed-note.py "path"    # Index
.venv/bin/python3 .2ndBrain/skills/ocr-images.py           # Image → text
.venv/bin/python3 .2ndBrain/skills/json-to-markdown.py     # JSON → md
```

---

*Last updated: 2026-02-01*
