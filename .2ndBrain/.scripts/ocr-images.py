#!/usr/bin/env python3
"""
OCR Images from Markdown Files
Extracts text from images referenced in markdown files using Tesseract OCR.
Usage: python3 0-Second-Brain/scripts/ocr-images.py "path/to/file.md"
"""

import pytesseract
from PIL import Image
from pathlib import Path
import re
import sys

def find_images_in_markdown(md_path):
    """Find all image references in a markdown file."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find markdown image syntax: ![alt](path) or ![alt](path "title")
    md_images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
    
    # Find Obsidian wiki-link syntax: ![[image.png]] or ![[image.png|alt text]]
    obsidian_images = re.findall(r'!\[\[([^\]|]+)(?:\|([^\]]*))?\]\]', content)
    
    # Find HTML img tags: <img src="path">
    html_images = re.findall(r'<img[^>]+src=["\'](.[^"\']+)["\']', content)
    
    # Combine and extract paths
    image_paths = []
    for alt, path in md_images:
        # Remove title if present
        path = path.split('"')[0].strip()
        image_paths.append((alt, path))
    
    for path, alt in obsidian_images:
        # Obsidian wiki-links are relative to the vault root
        image_paths.append((alt or "", path.strip()))
    
    for path in html_images:
        image_paths.append(("", path))
    
    return image_paths

def ocr_image(image_path, base_path):
    """Run OCR on a single image."""
    try:
        # Resolve relative paths
        if not Path(image_path).is_absolute():
            image_path = base_path.parent / image_path
        
        image_path = Path(image_path)
        
        if not image_path.exists():
            return f"❌ Image not found: {image_path}"
        
        # Open image
        img = Image.open(image_path)
        
        # Handle MPO format (Multi-Picture Object from some iPhones/cameras)
        # MPO files contain multiple frames; we want the first one
        if img.format == 'MPO':
            img.seek(0)  # Ensure we're at the first frame
            # Create a new image from the current frame to avoid format issues
            img = img.copy()
        
        # Convert to RGB if needed (handles various color modes)
        if img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')
        
        # Run OCR
        text = pytesseract.image_to_string(img)
        
        return text.strip()
        
    except Exception as e:
        return f"❌ Error processing {image_path.name}: {str(e)}"

def process_markdown_with_ocr(md_path):
    """Process a markdown file and extract text from all images."""
    md_path = Path(md_path)
    
    if not md_path.exists():
        print(f"❌ File not found: {md_path}", file=sys.stderr)
        return False
    
    print(f"📄 Processing: {md_path.name}")
    print("=" * 60)
    
    # Find all images
    images = find_images_in_markdown(md_path)
    
    if not images:
        print("⚠️  No images found in markdown file.")
        return False
    
    print(f"🖼️  Found {len(images)} image(s)\n")
    
    # Process each image
    results = []
    for i, (alt, img_path) in enumerate(images, 1):
        print(f"Processing image {i}/{len(images)}: {Path(img_path).name}")
        
        text = ocr_image(img_path, md_path)
        
        results.append({
            'alt': alt,
            'path': img_path,
            'text': text
        })
        
        # Show preview
        preview = text[:100].replace('\n', ' ')
        if len(text) > 100:
            preview += "..."
        print(f"  ✓ Extracted: {preview}\n")
    
    # Create output markdown
    output_path = md_path.parent / f"{md_path.stem}-ocr.md"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# OCR Results: {md_path.name}\n\n")
        f.write(f"**Date**: {Path().cwd()}\n")
        f.write(f"**Source**: {md_path.name}\n")
        f.write(f"**Images Processed**: {len(results)}\n\n")
        f.write("---\n\n")
        
        for i, result in enumerate(results, 1):
            f.write(f"## Image {i}: {Path(result['path']).name}\n\n")
            
            if result['alt']:
                f.write(f"**Alt Text**: {result['alt']}\n\n")
            
            f.write(f"**Extracted Text:**\n\n")
            f.write("```\n")
            f.write(result['text'])
            f.write("\n```\n\n")
            f.write("---\n\n")
        
        f.write("## Notes\n\n")
        f.write("*Review the extracted text above and process into appropriate lists or memos:*\n\n")
        f.write("- **Contacts** → Add to `2-Lists/Contacts.md`\n")
        f.write("- **Tasks** → Add to `2-Lists/Tasks.md`\n")
        f.write("- **Ideas** → Add to relevant list in `2-Lists/`\n")
        f.write("- **Quotes/Notes** → Create memo in `3-Memos/`\n")
        f.write("- **Other** → Process as needed\n\n")
        f.write("---\n\n")
        f.write("*OCR performed with Tesseract*\n")
    
    print(f"✅ Created: {output_path}")
    print(f"\n📝 Next steps:")
    print(f"   1. Review extracted text in: {output_path.name}")
    print(f"   2. Ask Cline to parse content and update appropriate lists")
    print(f"   3. Move original file to appropriate folder")
    
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 0-Second-Brain/scripts/ocr-images.py <markdown-file>", file=sys.stderr)
        print("\nExample:")
        print("  python3 0-Second-Brain/scripts/ocr-images.py 'notes-with-images.md'")
        sys.exit(1)
    
    success = process_markdown_with_ocr(sys.argv[1])
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
