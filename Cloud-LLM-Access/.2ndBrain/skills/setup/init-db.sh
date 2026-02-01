#!/bin/bash
# Second Brain - Initialize Vector Database
# Non-interactive. Creates empty ChromaDB for semantic search.
# Must run from vault root (parent of Cloud-LLM-Access/).
# Usage: bash Cloud-LLM-Access/.2ndBrain/skills/setup/init-db.sh

set -e

CLOUD_DIR="Cloud-LLM-Access"

# --- Validate location ---
if [ ! -d "$CLOUD_DIR/.2ndBrain" ]; then
  echo "ERROR: Must run from vault root (the folder containing Cloud-LLM-Access/)."
  exit 1
fi

echo "=== Second Brain: Initializing Vector Database ==="
echo ""

# --- Ensure Python environment exists ---
PYTHON="$CLOUD_DIR/.venv/bin/python"
if [ ! -f "$PYTHON" ]; then
  echo "ERROR: Python environment not found. Run setup-python.sh first."
  exit 1
fi

# --- Initialize database ---
if [ -f "$CLOUD_DIR/.chroma/chroma.sqlite3" ]; then
  echo "Vector database already initialized."
else
  mkdir -p "$CLOUD_DIR/.chroma"
  $PYTHON "$CLOUD_DIR/.2ndBrain/skills/init-vector-db.py"
  echo "Vector database initialized."
fi

echo ""
echo "=== Vector database ready ==="
