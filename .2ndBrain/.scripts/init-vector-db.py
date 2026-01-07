#!/usr/bin/env python3
"""
Initialize Vector Database for Second Brain
Creates ChromaDB and embeds all existing markdown files.
Run once during setup.
"""

import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
import sys

def init_vector_db():
    """Initialize the vector database and embed all existing notes."""
    
    print("🚀 Initializing Vector Database...")
    
    # Setup paths (scripts are in 0-Second-Brain/scripts/, DB is at root)
    base_path = Path(__file__).parent.parent.parent  # Go up to 2nd Brain root
    db_path = base_path / ".chroma"  # .chroma/ at root level
    
    # Initialize ChromaDB
    print(f"📁 Creating database at: {db_path}")
    client = chromadb.PersistentClient(path=str(db_path))
    
    # Create or get collection
    collection = client.get_or_create_collection(
        name="notes",
        metadata={"description": "Second Brain notes and transcriptions"}
    )
    
    # Load embedding model
    print("🤖 Loading embedding model (sentence-transformers/all-MiniLM-L6-v2)...")
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    # Find all markdown files to embed
    markdown_dirs = [
        base_path / "1-Raw" / "md",
        base_path / "2-Lists",
        base_path / "3-Memos",
        base_path / "4-Wisdom"
    ]
    
    all_files = []
    for md_dir in markdown_dirs:
        if md_dir.exists():
            all_files.extend(list(md_dir.glob("*.md")))
    
    if not all_files:
        print("⚠️  No markdown files found to embed.")
        return
    
    print(f"📝 Found {len(all_files)} markdown files to embed...")
    
    # Embed each file
    embedded_count = 0
    for file_path in all_files:
        try:
            # Read content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip empty files
            if not content.strip():
                continue
            
            # Generate embedding
            embedding = model.encode(content, convert_to_tensor=False)
            
            # Create unique ID from file path
            file_id = str(file_path.relative_to(base_path)).replace('/', '_')
            
            # Store in database
            collection.upsert(
                embeddings=[embedding.tolist()],
                documents=[content],
                metadatas=[{
                    "file": str(file_path.relative_to(base_path)),
                    "filename": file_path.name,
                    "directory": file_path.parent.name
                }],
                ids=[file_id]
            )
            
            embedded_count += 1
            print(f"  ✓ {file_path.relative_to(base_path)}")
            
        except Exception as e:
            print(f"  ✗ Error embedding {file_path.name}: {e}")
    
    print(f"\n✅ Successfully embedded {embedded_count}/{len(all_files)} files")
    print(f"📊 Database location: {db_path}")
    print(f"🔍 Ready for semantic search!")

if __name__ == "__main__":
    try:
        init_vector_db()
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
