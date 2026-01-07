#!/usr/bin/env python3
"""
Convert WhisperX JSON transcription to readable Markdown format.
Usage: python3 0-Second-Brain/scripts/json-to-markdown.py "1-Raw/json/FILENAME.json"
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def json_to_markdown(json_path):
    """Convert WhisperX JSON to readable Markdown."""
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    segments = data.get('segments', [])
    language = data.get('language', 'Unknown')
    filename = Path(json_path).stem
    
    if segments:
        duration = segments[-1]['end'] - segments[0]['start']
        speakers = set()
        for seg in segments:
            if 'speaker' in seg:
                speakers.add(seg['speaker'])
        num_speakers = len(speakers)
    else:
        duration = 0
        num_speakers = 0
    
    full_transcript = ' '.join([seg['text'].strip() for seg in segments])
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    md = f"# Transcription: {filename}\n\n"
    md += f"**Date**: {date_str}  \n"
    md += f"**Duration**: ~{int(duration)} seconds  \n"
    md += f"**Language**: {language.upper()}  \n"
    md += f"**Speakers**: {num_speakers}"
    
    if num_speakers > 0 and speakers:
        speaker_list = ', '.join(sorted(speakers))
        md += f" ({speaker_list})"
    
    md += "\n\n---\n\n"
    md += "## Full Transcript\n\n"
    md += f"> {full_transcript}\n\n"
    md += "---\n\n"
    md += "## Detailed Transcript with Timestamps\n\n"
    
    for segment in segments:
        speaker = segment.get('speaker', 'UNKNOWN')
        start = segment['start']
        end = segment['end']
        
        md += f"### {speaker} ({start:.1f}s - {end:.1f}s)\n\n"
        
        if 'words' in segment:
            md += "| Time | Word | Confidence |\n"
            md += "|------|------|------------|\n"
            
            for word in segment['words']:
                w_start = word['start']
                w_end = word['end']
                w_text = word['word']
                w_score = word.get('score', 0) * 100
                md += f"| {w_start:.2f}s - {w_end:.2f}s | {w_text} | {w_score:.1f}% |\n"
            
            md += "\n"
    
    md += "---\n\n"
    md += "## Notes\n\n"
    md += "*Add your notes and action items here*\n\n"
    md += "---\n\n"
    md += "*Transcribed with WhisperX (diarization enabled)*  \n"
    md += f"*Source JSON: `{Path(json_path).name}`*\n"
    
    return md

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 0-Second-Brain/scripts/json-to-markdown.py <json_file>")
        sys.exit(1)
    
    json_path = sys.argv[1]
    
    if not Path(json_path).exists():
        print(f"Error: File not found: {json_path}")
        sys.exit(1)
    
    markdown = json_to_markdown(json_path)
    
    # Save to 1-Raw/md/ with same filename
    json_file = Path(json_path)
    md_path = Path('1-Raw/md') / f"{json_file.stem}.md"
    
    with open(md_path, 'w') as f:
        f.write(markdown)
    
    print(f"✅ Created: {md_path}")
    
    # Auto-embed into vector database
    try:
        import subprocess
        embed_script = Path(__file__).parent / "embed-note.py"  # Now in same scripts folder
        result = subprocess.run(
            ["python3", str(embed_script), str(md_path)],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print(f"⚠️  Warning: Could not embed note: {result.stderr.strip()}")
    except Exception as e:
        print(f"⚠️  Warning: Could not auto-embed note: {e}")

if __name__ == "__main__":
    main()
