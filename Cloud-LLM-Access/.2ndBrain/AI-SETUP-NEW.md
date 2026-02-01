# Second Brain Setup - New Vault

You are helping a user set up Second Brain in a new Obsidian vault.
Run each command below in order. If any command fails, stop and tell the user what went wrong.

## Step 1: Install Dependencies

```bash
bash Cloud-LLM-Access/.2ndBrain/skills/setup/install-dependencies.sh --model MODEL_PLACEHOLDER
```

## Step 2: Set Up Python

```bash
bash Cloud-LLM-Access/.2ndBrain/skills/setup/setup-python.sh
```

## Step 3: Create Folders

```bash
bash Cloud-LLM-Access/.2ndBrain/skills/setup/create-folders.sh --folders FOLDERS_PLACEHOLDER
```

## Step 4: Initialize Vector Database

```bash
bash Cloud-LLM-Access/.2ndBrain/skills/setup/init-db.sh
```

## Step 5: Tell the User

When all steps complete, tell the user:

- Setup complete.
- Open Obsidian and select this folder as your vault.
- Your files at vault root are private (local model only).
- Folders created in Cloud-LLM-Access/ for cloud processing.
- Edit Cloud-LLM-Access/.env to add your HuggingFace token (needed for transcription).
- You can rename, delete, or add folders in Cloud-LLM-Access/ anytime.

## If Something Fails

- If uv or Ollama fails to install, tell the user to check their internet connection.
- If Python 3.9 can't be found, tell the user: uv will download it automatically.
- If Ollama model pull fails, tell the user to try: ollama pull <model> manually.
- Do NOT skip steps. Each depends on the previous one.
