#!/usr/bin/env python3
"""
Compile all text sources into RAW-TEXT.md for human review.
HARD-CODED STOP: This script exits after creating RAW-TEXT.md.
User must review and approve before AI proceeds to planning.

Usage: python3 0-Second-Brain/scripts/compile-raw-text.py
"""

import json
import subprocess
from pathlib import Path

def run_command(cmd):
    """Run a command silently."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

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
    
    # Markdown files (exclude system files)
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
    output += "**Next Step: Review this file, fix any transcription errors, then tell AI: 'approved'**\n"
    output += "**AI will then read RAW-TEXT.md and create PROCESSING-PLAN.md using semantic search**\n"
    return output

def main():
    root_dir = Path(".")
    
    print("📊 Scanning root directory...")
    
    # Find all files at root
    m4a_files = list(root_dir.glob("*.m4a"))
    
    # Exclude system markdown files
    all_md_files = list(root_dir.glob("*.md"))
    md_files = [f for f in all_md_files if f.name not in ['RAW-TEXT.md', 'PROCESSING-PLAN.md']]
    
    pdf_files = list(root_dir.glob("*.pdf"))
    image_files = list(root_dir.glob("*.jpg")) + list(root_dir.glob("*.jpeg")) + list(root_dir.glob("*.png"))
    
    print(f"🎵 Audio files (.m4a): {len(m4a_files)}")
    print(f"📝 Markdown files (.md): {len(md_files)}")
    print(f"📄 PDF files (.pdf): {len(pdf_files)}")
    print(f"🖼️  Image files: {len(image_files)}")
    
    # CHECK: Ensure all audio files have been transcribed first
    if m4a_files:
        untranscribed = []
        for m4a_file in m4a_files:
            json_file = root_dir / f"{m4a_file.stem}.json"
            if not json_file.exists():
                untranscribed.append(m4a_file.name)
        
        if untranscribed:
            print(f"\n{'='*60}")
            print(f"❌ ERROR: Audio files must be transcribed first!")
            print(f"{'='*60}")
            print(f"\n🎵 Found {len(untranscribed)} untranscribed audio file(s):")
            for filename in untranscribed:
                print(f"   - {filename}")
            print(f"\n📝 You must run transcription BEFORE compilation:")
            print(f"   .venv/bin/python3 .2ndBrain/.scripts/transcribe.py")
            print(f"\n💡 Transcription converts audio → JSON files")
            print(f"   Then this script compiles all text sources")
            print(f"{'='*60}\n")
            exit(1)
    
    if not any([m4a_files, md_files, pdf_files, image_files]):
        print("\n✅ No files to process at root")
        return
    
    # OCR markdown files with image references
    if md_files:
        print(f"\n📷 Checking markdown files for images...")
        for md_file in md_files:
            try:
                with open(md_file, 'r') as f:
                    if any(x in f.read() for x in ['![', '.jpg', '.jpeg', '.png']):
                        print(f"   🔍 OCR processing: {md_file.name}")
                        cmd = f'python3 0-Second-Brain/scripts/ocr-images.py "{md_file.name}"'
                        run_command(cmd)
            except:
                pass
    
    # OCR standalone images
    if image_files:
        print(f"\n🖼️  Processing {len(image_files)} standalone images...")
        for img_file in image_files:
            # Create temp markdown file with image reference
            temp_md = Path(f"{img_file.stem}.md")
            with open(temp_md, 'w') as f:
                f.write(f"![[{img_file.name}]]")
            cmd = f'python3 0-Second-Brain/scripts/ocr-images.py "{temp_md.name}"'
            run_command(cmd)
    
    # Compile all extracted text
    print(f"\n📋 Compiling all extracted text...")
    raw_text = create_raw_text(m4a_files, md_files, image_files, root_dir)
    output_file = Path("RAW-TEXT.md")
    with open(output_file, 'w') as f:
        f.write(raw_text)
    
    print(f"✅ Saved: {output_file}")
    print(f"\n{'='*60}")
    print(f"⏸️  HARD STOP: Human review required")
    print(f"{'='*60}")
    print(f"📝 Review RAW-TEXT.md and fix any transcription errors")
    print(f"{'='*60}\n")
    
    # HARD-CODED HUMAN-IN-THE-LOOP: Cannot proceed without approval
    while True:
        approval = input("Type 'approved' to continue (or 'exit' to stop): ").strip().lower()
        if approval == 'approved':
            print("\n✅ Approval received. AI can now proceed to create PROCESSING-PLAN.md")
            print("🤖 Tell AI: 'approved' to continue\n")
            break
        elif approval == 'exit':
            print("\n❌ Process cancelled. Review RAW-TEXT.md when ready.\n")
            exit(1)
        else:
            print("❌ Invalid input. Please type 'approved' or 'exit'")

if __name__ == "__main__":
    main()
