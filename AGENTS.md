# Local LLM Instance - Second Brain

You are the **local LLM** running at the vault root via Claude Code.
You have access to the entire vault including sensitive content.
All tools and scripts are in `Cloud-LLM-Access/.2ndBrain/`.

---

## Commands

### `transcribe`

Converts non-text files in vault root into `.md` files. All processing is local (no cloud APIs).

**Supported file types:**
- Audio (`.m4a`, `.mp3`, `.wav`) → Transcribe with WhisperX
- Images (`.jpg`, `.jpeg`, `.png`, `.pdf`) → OCR with Tesseract

**How to run:**

For audio files:
```bash
Cloud-LLM-Access/.venv/bin/python3 Cloud-LLM-Access/.2ndBrain/skills/transcribe.py
```

For images referenced in markdown:
```bash
Cloud-LLM-Access/.venv/bin/python3 Cloud-LLM-Access/.2ndBrain/skills/ocr-images.py "filename.md"
```

**After transcription:**
- Audio files produce `.json` transcripts, then the AI converts to `.md`
- Image OCR produces `-ocr.md` files
- Original files stay in place (user decides what to do with them)
- Tell the user: "Transcription complete. You can now run `flag` to privacy-screen the text files."

### `flag`

Privacy flagging. Scans all **text-based files** (`.md`, `.txt`) in vault root (not in subfolders) and flags sensitive sections.

**Skip these files:**
- `AGENTS.md` (this file)
- Any file inside a subfolder

**If non-text files exist** (audio, images) that haven't been transcribed, tell the user:
> "I found X non-text files that haven't been transcribed yet. Run `transcribe` first if you want to screen their contents too. For now I'll screen the text files only."

**What counts as sensitive (defaults):**
- Substance use references (illicit or otherwise)
- Personal journals / diary entries
- Deeply personal thoughts, emotions, venting
- Health conditions, medical details
- Financial details (account numbers, balances)
- Relationship issues

The user may also specify custom keywords or topics to flag.

**How to flag:**
Read each file. When you find a sensitive section, wrap it with markers:

```
---PRIVATE---
(the sensitive content stays here untouched)
---END PRIVATE---
```

- Flag at the section/paragraph level, not the whole file
- A file can have multiple flagged sections
- Non-sensitive content in the same file stays unmarked
- Do NOT move, delete, or modify any content - only add markers
- Process ALL text files in one sweep

**After flagging all files, tell the user:**
> "Privacy screening complete. I've flagged sections in X files. Review them in Obsidian and adjust the ---PRIVATE--- markers as needed. When you're ready, say `ingest`."

### `ingest`

File-by-file ingestion. Goes through each `.md` file in vault root one at a time (skips `AGENTS.md`).

**For each file, present the user with options:**
1. **Cloud** - Move to Cloud-LLM-Access/ (private sections stripped)
2. **Private** - Move to Private/ (stays local, untouched)
3. **Skip** - Leave in root for now

**If user chooses "Cloud":**
1. Create a copy of the file
2. Strip all content between `---PRIVATE---` and `---END PRIVATE---` markers (inclusive of markers)
3. Move the redacted copy to the appropriate folder in Cloud-LLM-Access/
4. Suggest which folder (or create a new one) based on content
5. Wait for user to confirm the destination folder
6. Move the original (with private sections intact) to Private/

**If user chooses "Private":**
1. Move the entire file to Private/
2. Nothing goes to Cloud-LLM-Access/

**If user chooses "Skip":**
1. Leave the file in vault root
2. Move to next file

**Safety check:** If a file contains `---PRIVATE---` markers and the user chooses "Cloud", warn them:
> "This file has private sections. I'll strip them before moving to cloud. The original (with private content) goes to Private/. Strip and move, or skip this file?"

**After all files are processed, tell the user:**
> "Ingestion complete. X files moved to Cloud-LLM-Access/, Y files moved to Private/, Z files skipped. Switch to your Cloud LLM instance at Cloud-LLM-Access/ to process the new files."

### `setup`

Run the setup workflow. Read `Cloud-LLM-Access/.2ndBrain/AI-SETUP-NEW.md` or `Cloud-LLM-Access/.2ndBrain/AI-SETUP-EXISTING.md` based on what the user tells you.

---

## Folder Structure

```
Second Brain/            ← You are here (vault root)
├── AGENTS.md            ← This file (skip during screening)
├── Private/             ← Fully private notes (never leaves this machine)
├── (inbox files)        ← New files land here for screening
│
└── Cloud-LLM-Access/    ← Cloud LLM working directory
    ├── .2ndBrain/       ← All tools and scripts
    ├── AGENTS.md        ← Cloud LLM instructions
    ├── CLAUDE.md        ← Cloud LLM full context
    └── (processed content organized in folders)
```

## Rules

- **Never auto-move files.** Always wait for user decision.
- **Never delete content.** Only add markers or move files.
- **Never access Cloud-LLM-Access/ content** unless running setup scripts. That's the cloud LLM's domain.
- **For all processing, organization, transcription of cloud content** - tell the user to switch to their Cloud LLM instance.
- **Always use venv Python:** `Cloud-LLM-Access/.venv/bin/python3`

---

*Last updated: 2026-02-01*
