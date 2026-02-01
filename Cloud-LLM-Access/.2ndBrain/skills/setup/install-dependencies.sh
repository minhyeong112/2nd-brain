#!/bin/bash
# Second Brain - Install System Dependencies
# Non-interactive. Pass --model <name> to specify Ollama model.
# Usage: bash install-dependencies.sh --model llama3.2

set -e

MODEL="llama3.2"
while [[ $# -gt 0 ]]; do
  case $1 in
    --model) MODEL="$2"; shift 2 ;;
    *) shift ;;
  esac
done

echo "=== Second Brain: Installing Dependencies ==="
echo ""

# --- Detect OS ---
OS="unknown"
if [[ "$OSTYPE" == "darwin"* ]]; then
  OS="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
  OS="linux"
else
  echo "ERROR: Unsupported OS ($OSTYPE). macOS and Linux only."
  exit 1
fi
echo "Detected OS: $OS"

# --- Homebrew (macOS only) ---
if [[ "$OS" == "macos" ]] && ! command -v brew &> /dev/null; then
  echo "Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  echo "Homebrew installed."
fi

# --- Git ---
if command -v git &> /dev/null; then
  echo "git: already installed ($(git --version))"
else
  echo "Installing git..."
  if [[ "$OS" == "macos" ]]; then
    brew install git
  else
    sudo apt-get update && sudo apt-get install -y git
  fi
  echo "git: installed."
fi

# --- uv (Python package manager) ---
if command -v uv &> /dev/null; then
  echo "uv: already installed ($(uv --version))"
else
  echo "Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
  echo "uv: installed."
fi

# --- ffmpeg (audio processing) ---
if command -v ffmpeg &> /dev/null; then
  echo "ffmpeg: already installed"
else
  echo "Installing ffmpeg..."
  if [[ "$OS" == "macos" ]]; then
    brew install ffmpeg
  else
    sudo apt-get update && sudo apt-get install -y ffmpeg
  fi
  echo "ffmpeg: installed."
fi

# --- tesseract (OCR) ---
if command -v tesseract &> /dev/null; then
  echo "tesseract: already installed"
else
  echo "Installing tesseract..."
  if [[ "$OS" == "macos" ]]; then
    brew install tesseract
  else
    sudo apt-get update && sudo apt-get install -y tesseract-ocr
  fi
  echo "tesseract: installed."
fi

# --- Ollama ---
if command -v ollama &> /dev/null; then
  echo "ollama: already installed"
else
  echo "Installing Ollama..."
  if [[ "$OS" == "macos" ]]; then
    brew install ollama
  else
    curl -fsSL https://ollama.com/install.sh | sh
  fi
  echo "ollama: installed."
fi

# --- Pull local model ---
echo "Pulling Ollama model: $MODEL (this may take a few minutes)..."
ollama pull "$MODEL"
echo "Model $MODEL: ready."

echo ""
echo "=== Dependencies installed successfully ==="
