# Cloud LLM Instance - Second Brain

You are the **cloud LLM** inside `Cloud-LLM-Access/`.
**NEVER access parent directory (`../`).** Sensitive content lives there.
All content here is pre-screened and safe to process.

---

## `organize`

If there are `.md` files in this directory root, go through each one at a time. Skip `AGENTS.md`, `CLAUDE.md`, `.2ndBrain/`, and files already in subfolders.

For each file:
1. Read it. Summarize contents.
2. Search for related content: `.venv/bin/python3 .2ndBrain/skills/semantic-search.py "query"`
3. Suggest folder placement (new or merge with existing file).
4. **Present plan. Wait for user approval.**
5. **Re-read file from disk** (user may have edited during review).
6. Execute: create/edit files in destination folder.
7. Index: `.venv/bin/python3 .2ndBrain/skills/embed-note.py "path"`
8. Move original to `.Archive/`, delete from root.

For full workflow details, read `.2ndBrain/AI-WORKFLOW.md`.

---

## Rules

- One file at a time. Never batch.
- User approves every action. Never auto-move.
- Re-read files after approval (user edits in Obsidian).
- One layer deep: `Tasks-Urgent.md`, not nested subheadings.
- File naming: `Title-Case-With-Dashes.md`
- User decides folder structure. Suggest, don't impose.
- Always use `.venv/bin/python3` for scripts.

## If Something Looks Wrong

If anything seems broken or missing, tell the user to re-run the setup process from the Second Brain website.

---

*Last updated: 2026-02-01*
