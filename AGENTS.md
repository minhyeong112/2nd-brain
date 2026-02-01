# Local LLM Instance - Second Brain

You are the **local LLM** at the vault root.
All tools and scripts are in `Cloud-LLM-Access/.2ndBrain/`.

---

## Commands

### `transcribe`

Converts non-text files in vault root into `.md` files. All processing is local (no cloud APIs).

For audio files:
```bash
Cloud-LLM-Access/.venv/bin/python3 Cloud-LLM-Access/.2ndBrain/skills/transcribe.py
```

For images referenced in markdown:
```bash
Cloud-LLM-Access/.venv/bin/python3 Cloud-LLM-Access/.2ndBrain/skills/ocr-images.py "filename.md"
```

After: tell user to run `flag` to privacy-screen the text files.

### `flag`

Scans all text files (`.md`, `.txt`) in vault root (not subfolders). Skip `AGENTS.md`. If untranscribed non-text files exist, warn user to run `transcribe` first.

Read each file. Wrap sensitive sections with:

```
---PRIVATE---
(sensitive content untouched)
---END PRIVATE---
```

**Sensitive by default:** substance use, journals, personal thoughts, health details, financial details, relationships. User may add custom topics.

Flag at section level, not whole file. Only add markers - never move/delete/modify content. Process all files in one sweep.

After: "Flagged X files. Review in Obsidian, adjust markers. Say `ingest` when ready."

### `ingest`

Go through each `.md` file in vault root one at a time (skip `AGENTS.md`). For each file ask:

1. **Cloud** → Strip `---PRIVATE---` sections, move redacted copy to `Cloud-LLM-Access/` root. Original goes to `Private/`.
2. **Private** → Move whole file to `Private/`.
3. **Skip** → Leave in root.

If file has `---PRIVATE---` markers and user picks Cloud, warn: "This has private sections. I'll strip them. Original goes to Private/. Proceed or skip?"

After all files: "Done. X cloud, Y private, Z skipped. Switch to Cloud LLM to organize."

---

## Rules

- Never auto-move. Always wait for user decision.
- Never delete content. Only add markers or move files.
- Never access Cloud-LLM-Access/ content. That's the cloud LLM's domain.
- For organization/processing, tell user to switch to Cloud LLM instance.

## If Something Looks Wrong

If `Private/`, `Cloud-LLM-Access/.venv/`, or `Cloud-LLM-Access/.Archive/` are missing, tell the user to re-run the setup process from the Second Brain website.

---

*Last updated: 2026-02-01*
