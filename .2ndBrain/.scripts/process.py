#!/usr/bin/env python3
"""
Second Brain processor: transcribe audio, OCR images, extract markdown text.
Compiles all raw text into RAW-TEXT.md for user review.
AI then reads RAW-TEXT.md and creates PROCESSING-PLAN.md using semantic search.
Usage: python3 0-Second-Brain/scripts/process.py
"""

import os
import subprocess
import json
import sys
import threading
import time
import psutil
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
HF_TOKEN = os.getenv('HF_TOKEN')

if not HF_TOKEN or HF_TOKEN == 'your_huggingface_token_here':
    print("❌ Error: HuggingFace token not configured")
    print("   Please edit .env file and add your HF_TOKEN")
    print("   Get token from: https://huggingface.co/settings/tokens")
    sys.exit(1)

def run_command(cmd, show_output=False):
    """Run a command silently."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def run_command_with_progress(cmd, description="Processing"):
    """Run command with live progress feedback."""
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    def show_progress():
        start_time = time.time()
        spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
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
        
        # Final elapsed time
        elapsed = time.time() - start_time
        mins, secs = divmod(int(elapsed), 60)
        if mins > 0:
            time_str = f"{mins}m {secs}s"
        else:
            time_str = f"{secs}s"
        print(f"\r   ✓ {description} complete ({time_str})                    ")
    
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
    """
    Preprocess audio to 16kHz mono WAV and trim silences.
    This dramatically improves WhisperX performance.
    Returns True if successful.
    """
    # Get original duration
    original_duration = get_audio_duration(input_file)
    
    # ffmpeg command - MORE AGGRESSIVE silence removal:
    # 1. Convert to 16kHz mono WAV
    # 2. Remove silence aggressively:
    #   - start_threshold=-40dB (was -50dB, now more sensitive)
    #   - stop_duration=0.3s (was 0.5s, now removes more pauses)
    #   - Detection window 0.2s (faster detection)
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
    
    print(f"   🔧 Preprocessing (16kHz mono + aggressive silence removal)...", flush=True)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0 and Path(output_file).exists():
        processed_duration = get_audio_duration(output_file)
        time_saved = original_duration - processed_duration
        
        if time_saved > 0:
            percent_saved = (time_saved / original_duration) * 100
            mins_saved, secs_saved = divmod(int(time_saved), 60)
            if mins_saved > 0:
                time_saved_str = f"{mins_saved}m {secs_saved}s"
            else:
                time_saved_str = f"{secs_saved}s"
            
            orig_mins, orig_secs = divmod(int(original_duration), 60)
            proc_mins, proc_secs = divmod(int(processed_duration), 60)
            print(f"   ✅ Removed {time_saved_str} of silence ({percent_saved:.1f}%) • {orig_mins}:{orig_secs:02d} → {proc_mins}:{proc_secs:02d}")
        else:
            print(f"   ✅ Preprocessed (minimal silence detected)")
        return True
    else:
        print(f"   ⚠️  Preprocessing failed, will use original file")
        return False

def get_transcript(json_path):
    """Extract clean transcript from JSON."""
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        segments = data.get('segments', [])
        return ' '.join([seg['text'].strip() for seg in segments])
    except:
        return "Error reading transcript"

def create_raw_text(m4a_files, md_files, image_files, root_dir):
    """Compile ALL extracted text: transcripts with speakers, OCR, markdown content."""
    output = "# 🗂️ Raw Text (Transcripts, Markdown, OCR)\n\n"
    output += f"**Generated from {len(m4a_files)} audio, {len(md_files)} markdown, {len(image_files)} images**\n\n"
    output += "---\n\n"
    
    # Audio transcripts - read directly from JSON to get speaker info (from root)
    if m4a_files:
        output += "## 🎵 Audio Transcripts\n\n"
        for i, m4a_file in enumerate(m4a_files, 1):
            json_file = root_dir / f"{m4a_file.stem}.json"
            output += f"### [{i}] {m4a_file.name}\n\n"
            
            if json_file.exists():
                try:
                    with open(json_file, 'r') as f:
                        data = json.load(f)
                    
                    segments = data.get('segments', [])
                    if segments:
                        current_speaker = None
                        for seg in segments:
                            speaker = seg.get('speaker', 'SPEAKER_00')
                            text = seg.get('text', '').strip()
                            
                            # Show speaker label when speaker changes
                            if speaker != current_speaker:
                                output += f"\n**{speaker}:** "
                                current_speaker = speaker
                            
                            output += text + " "
                        output += "\n\n"
                    else:
                        output += "*No transcript available*\n\n"
                except Exception as e:
                    output += f"*Error reading transcript: {e}*\n\n"
            else:
                output += "*JSON file not found*\n\n"
    
    # Markdown files
    if md_files:
        output += "## 📝 Markdown Files\n\n"
        for i, md_file in enumerate(md_files, 1):
            try:
                with open(md_file, 'r') as f:
                    content = f.read()
                output += f"### [{i}] {md_file.name}\n{content}\n\n"
            except:
                output += f"### [{i}] {md_file.name}\nError reading\n\n"
    
    # OCR results (check for -ocr.md files)
    ocr_files = list(root_dir.glob("*-ocr.md"))
    if ocr_files:
        output += "## 🖼️ OCR Extracted Text\n\n"
        for i, ocr_file in enumerate(ocr_files, 1):
            try:
                with open(ocr_file, 'r') as f:
                    content = f.read()
                output += f"### [{i}] {ocr_file.name}\n{content}\n\n"
            except:
                output += f"### [{i}] {ocr_file.name}\nError reading\n\n"
    
    output += "---\n\n"
    output += "**AI: Read all text above and create PROCESSING-PLAN.md with specific actions**\n"
    return output

def main():
    root_dir = Path(".")
    raw_json_dir = Path("1-Raw/json")
    raw_md_dir = Path("1-Raw/md")

    # Step 1: Scan and count files at root
    print("📊 Scanning root directory...")

    m4a_files = list(root_dir.glob("*.m4a"))
    md_files = list(root_dir.glob("*.md"))
    pdf_files = list(root_dir.glob("*.pdf"))
    image_files = list(root_dir.glob("*.jpg")) + list(root_dir.glob("*.jpeg")) + list(root_dir.glob("*.png"))

    print(f"🎵 Audio files (.m4a): {len(m4a_files)}")
    print(f"📝 Markdown files (.md): {len(md_files)}")
    print(f"📄 PDF files (.pdf): {len(pdf_files)}")
    print(f"🖼️  Image files: {len(image_files)}")

    if not any([m4a_files, md_files, pdf_files, image_files]):
        print("✅ No files to process at root")
        return

    # Step 2: Transcribe all audio files (output to root)
    if m4a_files:
        print(f"\n🎵 Processing {len(m4a_files)} audio files...")
        for i, m4a_file in enumerate(m4a_files, 1):
            json_path = root_dir / f"{m4a_file.stem}.json"
            file_size_mb = m4a_file.stat().st_size / (1024 * 1024)
            print(f"\n[{i}/{len(m4a_files)}] {m4a_file.name} ({file_size_mb:.2f}MB)")
            
            # Always process - anything in root needs transcription
            # Preprocess audio first (huge performance boost)
            preprocessed_wav = Path(f"temp_{m4a_file.stem}.wav")
            preprocess_success = preprocess_audio(m4a_file, preprocessed_wav)
            
            # Use preprocessed WAV if successful, otherwise original m4a
            input_file = preprocessed_wav if preprocess_success else m4a_file
            
            # Transcribe with progress feedback - output directly to root (upgraded to 'small' model)
            cmd = f'python3 -m whisperx "{input_file}" --model small --compute_type int8 --device cpu --diarize --hf_token {HF_TOKEN} --output_dir "." --output_format json --language en'
            success = run_command_with_progress(cmd, "Transcribing")
            
            # If we used a preprocessed file, rename the JSON to match original filename
            if preprocess_success:
                temp_json_path = root_dir / f"temp_{m4a_file.stem}.json"
                if temp_json_path.exists():
                    temp_json_path.rename(json_path)
            
            # Clean up preprocessed file
            if preprocessed_wav.exists():
                preprocessed_wav.unlink()
            
            # Check if JSON was actually created
            if json_path.exists():
                transcript = get_transcript(json_path)
                print(f"   ✅ Transcribed: \"{transcript[:60]}...\"")
            else:
                print(f"   ❌ Failed")

    # Step 3: OCR markdown files with image references
    if md_files:
        print(f"\n�️  Processing markdown with images...")
        for md_file in md_files:
            try:
                with open(md_file, 'r') as f:
                    if any(x in f.read() for x in ['![', '.jpg', '.jpeg', '.png']):
                        cmd = f'python3 0-Second-Brain/scripts/ocr-images.py "{md_file.name}"'
                        run_command(cmd)
            except:
                pass
        print("✅ OCR complete")
    
    # Step 5: OCR standalone images
    if image_files:
        print(f"\n🖼️  Processing {len(image_files)} standalone images...")
        for img_file in image_files:
            # Create temp markdown file with image reference
            temp_md = Path(f"{img_file.stem}.md")
            with open(temp_md, 'w') as f:
                f.write(f"![[{img_file.name}]]")
            cmd = f'python3 0-Second-Brain/scripts/ocr-images.py "{temp_md.name}"'
            run_command(cmd)
        print("✅ OCR complete")

    # Step 6: Compile all extracted text
    print(f"\n📋 Compiling all extracted text...")
    raw_text = create_raw_text(m4a_files, md_files, image_files, root_dir)
    output_file = Path("RAW-TEXT.md")
    with open(output_file, 'w') as f:
        f.write(raw_text)
    print(f"✅ Saved: {output_file}")
    print(f"\n⏸️  PAUSED: Review and edit RAW-TEXT.md to fix any errors")
    print(f"📝 Then tell AI: 'approved' or make edits first")
    print(f"🤖 AI will then read RAW-TEXT.md and create PROCESSING-PLAN.md (using semantic search)")

if __name__ == "__main__":
    main()
