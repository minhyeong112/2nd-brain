#!/bin/bash
# Second Brain - Set Up Python Environment
# Non-interactive. Uses uv for isolated Python 3.9.
# Must run from vault root (parent of Cloud-LLM-Access/).
# Usage: bash Cloud-LLM-Access/.2ndBrain/skills/setup/setup-python.sh

set -e

CLOUD_DIR="Cloud-LLM-Access"

# --- Validate location ---
if [ ! -d "$CLOUD_DIR/.2ndBrain" ]; then
  echo "ERROR: Must run from vault root (the folder containing Cloud-LLM-Access/)."
  exit 1
fi

echo "=== Second Brain: Setting Up Python Environment ==="
echo ""

# --- Ensure uv is available ---
if ! command -v uv &> /dev/null; then
  export PATH="$HOME/.local/bin:$PATH"
fi
if ! command -v uv &> /dev/null; then
  echo "ERROR: uv not found. Run install-dependencies.sh first."
  exit 1
fi

# --- Create venv with Python 3.9 ---
VENV_DIR="$CLOUD_DIR/.venv"

if [ -d "$VENV_DIR" ]; then
  echo "Python environment already exists at $VENV_DIR"
  echo "Skipping venv creation."
else
  echo "Creating Python 3.9 environment..."
  uv venv "$VENV_DIR" --python 3.9
  echo "Python environment created."
fi

# --- Install dependencies ---
echo "Installing Python packages (this may take several minutes)..."
uv pip install --python "$VENV_DIR/bin/python" -r "$CLOUD_DIR/.2ndBrain/requirements.txt"
echo "Python packages installed."

# --- Set up .env if missing ---
if [ ! -f "$CLOUD_DIR/.env" ]; then
  cp "$CLOUD_DIR/.2ndBrain/.env.example" "$CLOUD_DIR/.env"
  echo "Created .env from template. API keys need to be added."
else
  echo ".env already exists."
fi

echo ""
echo "=== Python environment ready ==="
