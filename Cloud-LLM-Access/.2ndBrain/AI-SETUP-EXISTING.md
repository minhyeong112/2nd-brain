# Second Brain Setup - Existing Vault

You are helping a user add Second Brain to their existing Obsidian vault.
Their files are already at vault root. Do NOT move, rename, or reorganize anything.
Run each command below in order. If any command fails, stop and tell the user what went wrong.

## Step 1: Install Dependencies

```bash
bash Cloud-LLM-Access/.2ndBrain/skills/setup/install-dependencies.sh
```

## Step 2: Set Up Python

```bash
bash Cloud-LLM-Access/.2ndBrain/skills/setup/setup-python.sh
```

## Step 3: Initialize Vector Database

```bash
bash Cloud-LLM-Access/.2ndBrain/skills/setup/init-db.sh
```

## Step 4: Tell the User

When all steps complete, tell the user:

- Setup complete.
- Your existing files are untouched and private (local model only).
- Cloud-LLM-Access/ is ready for cloud AI processing.
- Move or copy files into Cloud-LLM-Access/ when you're ready for cloud processing.
- No rush - migrate files gradually using privacy screening.
- Edit Cloud-LLM-Access/.env to add your HuggingFace token (needed for transcription).
- Create any folders you want inside Cloud-LLM-Access/.

## If Something Fails

- If uv fails to install, tell the user to check their internet connection.
- If Python 3.9 can't be found, tell the user: uv will download it automatically.
- Do NOT skip steps. Each depends on the previous one.
