#!/bin/bash
# Second Brain - Create Folder Structure (New Users Only)
# Non-interactive. Pass --folders with comma-separated list.
# Must run from vault root (parent of Cloud-LLM-Access/).
# Usage: bash Cloud-LLM-Access/.2ndBrain/skills/setup/create-folders.sh --folders Lists,Tasks,Memos,Contacts

set -e

CLOUD_DIR="Cloud-LLM-Access"
FOLDERS=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --folders) FOLDERS="$2"; shift 2 ;;
    *) shift ;;
  esac
done

# --- Validate location ---
if [ ! -d "$CLOUD_DIR/.2ndBrain" ]; then
  echo "ERROR: Must run from vault root (the folder containing Cloud-LLM-Access/)."
  exit 1
fi

if [ -z "$FOLDERS" ]; then
  echo "ERROR: No folders specified. Use --folders Lists,Tasks,Memos"
  exit 1
fi

echo "=== Second Brain: Creating Folder Structure ==="
echo ""

# --- Create each folder in Cloud-LLM-Access ---
IFS=',' read -ra FOLDER_LIST <<< "$FOLDERS"
for folder in "${FOLDER_LIST[@]}"; do
  folder=$(echo "$folder" | xargs)  # trim whitespace
  if [ -d "$CLOUD_DIR/$folder" ]; then
    echo "$folder/: already exists"
  else
    mkdir -p "$CLOUD_DIR/$folder"
    echo "$folder/: created"
  fi
done

echo ""
echo "=== Folders created in $CLOUD_DIR/ ==="
echo "You can rename, delete, or add more folders anytime."
