#!/usr/bin/env python3
"""
Transcribe audio files in vault root to JSON.
Run from vault root: Cloud-LLM-Access/.venv/bin/python3 Cloud-LLM-Access/.2ndBrain/skills/transcribe.py
"""

import subprocess
import threading
import time
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Determine vault root (where the script is called from)
VAULT_ROOT = Path(".")

# Load .env from Cloud-LLM-Access/
ENV_PATH = VAULT_ROOT / "Cloud-LLM-Access" / ".env"
load_dotenv(ENV_PATH)
HF_TOKEN = os.getenv("HF_TOKEN")

# Determine venv python path for whisperx subprocess
VENV_PYTHON = str(VAULT_ROOT / "Cloud-LLM-Access" / ".venv" / "bin" / "python3")

if not HF_TOKEN or HF_TOKEN == "your_huggingface_token_here":
    print("ERROR: HuggingFace token not configured")
    print(f"   Edit {ENV_PATH} and add your HF_TOKEN")
    print("   Get token from: https://huggingface.co/settings/tokens")
    sys.exit(1)

AUDIO_EXTENSIONS = ("*.m4a", "*.mp3", "*.wav")


def run_command_with_progress(cmd, description="Processing"):
    """Run command with live progress feedback."""
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def show_progress():
        start_time = time.time()
        spinner = ["|", "/", "-", "\\"]
        i = 0
        while process.poll() is None:
            elapsed = time.time() - start_time
            mins, secs = divmod(int(elapsed), 60)
            if mins > 0:
                time_str = f"{mins}m {secs}s"
            else:
                time_str = f"{secs}s"
            print(f"\r   {spinner[i % len(spinner)]} {description}... {time_str} elapsed", end="", flush=True)
            i += 1
            time.sleep(0.3)

        elapsed = time.time() - start_time
        mins, secs = divmod(int(elapsed), 60)
        if mins > 0:
            time_str = f"{mins}m {secs}s"
        else:
            time_str = f"{secs}s"
        print(f"\r   Done: {description} ({time_str})                    ")

    progress_thread = threading.Thread(target=show_progress, daemon=True)
    progress_thread.start()

    stdout, stderr = process.communicate()
    progress_thread.join(timeout=1)

    return process.returncode == 0


def get_audio_duration(file_path):
    """Get audio duration in seconds using ffprobe."""
    try:
        cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{file_path}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return float(result.stdout.strip())
    except:
        return 0


def preprocess_audio(input_file, output_file):
    """Preprocess audio to 16kHz mono WAV and trim silences."""
    original_duration = get_audio_duration(input_file)

    cmd = (
        f'ffmpeg -i "{input_file}" '
        f'-ar 16000 -ac 1 '
        f'-af "silenceremove='
        f'start_periods=1:start_duration=0.2:start_threshold=-40dB:'
        f'stop_periods=-1:stop_duration=0.3:stop_threshold=-40dB,'
        f'silenceremove=start_periods=0:start_duration=0:start_threshold=-40dB:'
        f'detection=peak" '
        f'-y "{output_file}" 2>&1'
    )

    print(f"   Preprocessing (16kHz mono + silence removal)...", flush=True)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode == 0 and Path(output_file).exists():
        processed_duration = get_audio_duration(output_file)
        time_saved = original_duration - processed_duration

        if time_saved > 0 and original_duration > 0:
            percent_saved = (time_saved / original_duration) * 100
            mins_saved, secs_saved = divmod(int(time_saved), 60)
            if mins_saved > 0:
                time_saved_str = f"{mins_saved}m {secs_saved}s"
            else:
                time_saved_str = f"{secs_saved}s"

            orig_mins, orig_secs = divmod(int(original_duration), 60)
            proc_mins, proc_secs = divmod(int(processed_duration), 60)
            print(f"   Removed {time_saved_str} of silence ({percent_saved:.1f}%) - {orig_mins}:{orig_secs:02d} to {proc_mins}:{proc_secs:02d}")
        else:
            print(f"   Preprocessed (minimal silence detected)")
        return True
    else:
        print(f"   WARNING: Preprocessing failed, will use original file")
        return False


def get_transcript(json_path):
    """Extract clean transcript from JSON."""
    try:
        import json
        with open(json_path, "r") as f:
            data = json.load(f)
        segments = data.get("segments", [])
        return " ".join([seg["text"].strip() for seg in segments])
    except:
        return "Error reading transcript"


def main():
    # Find all audio files in vault root
    audio_files = []
    for ext in AUDIO_EXTENSIONS:
        audio_files.extend(VAULT_ROOT.glob(ext))
    audio_files.sort()

    if not audio_files:
        print("No audio files found at vault root.")
        return

    print(f"Found {len(audio_files)} audio file(s) to transcribe\n")

    for i, audio_file in enumerate(audio_files, 1):
        json_path = VAULT_ROOT / f"{audio_file.stem}.json"
        file_size_mb = audio_file.stat().st_size / (1024 * 1024)
        print(f"[{i}/{len(audio_files)}] {audio_file.name} ({file_size_mb:.2f}MB)")

        # Skip if JSON already exists
        if json_path.exists():
            print(f"   Skipping (JSON already exists)")
            continue

        # Preprocess audio
        preprocessed_wav = VAULT_ROOT / f"temp_{audio_file.stem}.wav"
        preprocess_success = preprocess_audio(audio_file, preprocessed_wav)

        input_file = preprocessed_wav if preprocess_success else audio_file

        # Transcribe using venv python
        cmd = f'{VENV_PYTHON} -m whisperx "{input_file}" --model large-v3 --compute_type int8 --device cpu --diarize --hf_token {HF_TOKEN} --output_dir "." --output_format json --language en'
        success = run_command_with_progress(cmd, "Transcribing")

        # Rename JSON if temp file was used
        if preprocess_success:
            temp_json_path = VAULT_ROOT / f"temp_{audio_file.stem}.json"
            if temp_json_path.exists():
                temp_json_path.rename(json_path)

        # Clean up preprocessed file
        if preprocessed_wav.exists():
            preprocessed_wav.unlink()

        # Verify JSON was created
        if json_path.exists():
            transcript = get_transcript(json_path)
            preview = transcript[:80] + "..." if len(transcript) > 80 else transcript
            print(f"   Transcribed: \"{preview}\"")
        else:
            print(f"   FAILED to transcribe")

    print(f"\nTranscription complete!")
    print(f"Run `flag` to privacy-screen the text files.")


if __name__ == "__main__":
    main()
