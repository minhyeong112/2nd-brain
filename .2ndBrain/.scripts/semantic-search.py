#!/usr/bin/env python3
"""
Semantic Search across all notes in Second Brain
Uses vector similarity to find relevant content by meaning, not just keywords.
Usage: python3 0-Second-Brain/scripts/semantic-search.py "morning routines"
"""

import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
import sys

def semantic_search(query, n_results=10):
    """Search the vector database for semantically similar notes."""
    
    # Setup paths (scripts are in 0-Second-Brain/scripts/, DB is at root)
    base_path = Path(__file__).parent.parent.parent  # Go up to 2nd Brain root
    db_path = base_path / ".chroma"  # .chroma/ at root level
    
    # Check if database exists
    if not db_path.exists():
        print("❌ Vector database not initialized. Run: python3 0-Second-Brain/scripts/init-vector-db.py", file=sys.stderr)
        return False
    
    try:
        # Initialize ChromaDB
        client = chromadb.PersistentClient(path=str(db_path))
        collection = client.get_collection(name="notes")
        
        # Load embedding model
        print("🔍 Searching for:", query)
        print("=" * 60)
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        # Generate query embedding
        query_embedding = model.encode(query, convert_to_tensor=False)
        
        # Search database
        results = collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results
        )
        
        # Display results
        if not results['documents'][0]:
            print("No results found.")
            return True
        
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        ), 1):
            # Calculate similarity score (1 - distance, as lower distance = more similar)
            similarity = 1 - distance
            
            print(f"\n{i}. 📄 {metadata['file']} (similarity: {similarity:.2%})")
            print(f"   Directory: {metadata['directory']}")
            
            # Show relevant excerpt (first 200 chars)
            excerpt = doc[:200].replace('\n', ' ').strip()
            if len(doc) > 200:
                excerpt += "..."
            print(f"   Preview: {excerpt}")
            print("-" * 60)
        
        print(f"\n✅ Found {len(results['documents'][0])} relevant notes")
        return True
        
    except Exception as e:
        print(f"❌ Error searching: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 0-Second-Brain/scripts/semantic-search.py <search query>", file=sys.stderr)
        print("\nExamples:")
        print("  python3 0-Second-Brain/scripts/semantic-search.py \"productivity tips\"")
        print("  python3 0-Second-Brain/scripts/semantic-search.py \"morning routines\"")
        print("  python3 0-Second-Brain/scripts/semantic-search.py \"what I learned about habits\"")
        sys.exit(1)
    
    # Join all arguments as the query (allows multi-word queries without quotes)
    query = " ".join(sys.argv[1:])
    
    success = semantic_search(query)
    sys.exit(0 if success else 1)
