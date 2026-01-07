#!/usr/bin/env python3
"""
Embed a single note into the Vector Database
Called automatically after transcription or can be run manually.
Usage: python3 0-Second-Brain/scripts/embed-note.py "1-Raw/md/Recording_123.md"
"""

import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
import sys

def embed_note(file_path):
    """Embed a single markdown file into the vector database."""
    
    # Setup paths (scripts are in 0-Second-Brain/scripts/, DB is at root)
    base_path = Path(__file__).parent.parent.parent  # Go up to 2nd Brain root
    db_path = base_path / ".chroma"  # .chroma/ at root level
    file_path = Path(file_path)
    
    # Validate file exists
    if not file_path.exists():
        print(f"❌ File not found: {file_path}", file=sys.stderr)
        return False
    
    # Read content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}", file=sys.stderr)
        return False
    
    # Skip empty files
    if not content.strip():
        print(f"⚠️  Skipping empty file: {file_path.name}")
        return True
    
    try:
        # Initialize ChromaDB
        client = chromadb.PersistentClient(path=str(db_path))
        collection = client.get_or_create_collection(
            name="notes",
            metadata={"description": "Second Brain notes and transcriptions"}
        )
        
        # Load embedding model (cached after first load)
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        # Generate embedding
        embedding = model.encode(content, convert_to_tensor=False)
        
        # Create unique ID from file path
        try:
            relative_path = file_path.relative_to(base_path)
        except ValueError:
            # If file is not relative to base_path, use absolute path
            relative_path = file_path
        
        file_id = str(relative_path).replace('/', '_')
        
        # Store in database (upsert = update if exists, insert if new)
        collection.upsert(
            embeddings=[embedding.tolist()],
            documents=[content],
            metadatas=[{
                "file": str(relative_path),
                "filename": file_path.name,
                "directory": file_path.parent.name
            }],
            ids=[file_id]
        )
        
        print(f"✅ Embedded: {file_path.name}")
        return True
        
    except Exception as e:
        print(f"❌ Error embedding file: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 0-Second-Brain/scripts/embed-note.py <path-to-markdown-file>", file=sys.stderr)
        sys.exit(1)
    
    success = embed_note(sys.argv[1])
    sys.exit(0 if success else 1)
