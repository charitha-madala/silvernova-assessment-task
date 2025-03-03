from typing import List, Dict, Any, Tuple
from src.api import embed_texts
import logging
import re
import os
import json


logger = logging.getLogger('embed')

class EmbedService:

  def __init__(self, storage_path, chunk_size: int = 1000, chunk_overlap: int = 100):
        self.storage_path = storage_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.documents = self._load_documents()

  
  def _load_documents(self) -> List[Dict[str, Any]]:
        """Load documents from JSON file if it exists."""
        if os.path.exists('embedded_doc.json'):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse {self.storage_path}. Starting with empty document store.")
                return []
        return []
    
  def _save_documents(self) -> None:
      """Save documents to JSON file."""
      with open(self.storage_path, 'w', encoding='utf-8') as f:
          json.dump(self.documents, f, ensure_ascii=False)  


  def chunk_text(self, text: str) -> List[str]:
        """Split text into semantic chunks based on paragraphs and headers."""
       
        pattern = r'(#{1,6}.*?\n)|(\n\n)'
        splits = re.split(pattern, text)
            
        chunks = []
        current_chunk = ""
        
        for split in splits:
            if split and split.strip():
                if len(current_chunk) + len(split) > self.chunk_size and current_chunk:
                    chunks.append(current_chunk.strip())
                    # Keep some overlap for context
                    current_chunk = current_chunk[-self.chunk_overlap:] if self.chunk_overlap > 0 else ""
                
                current_chunk += split

        if current_chunk.strip():
            chunks.append(current_chunk.strip())
            
        return chunks
  
  def embed_and_store(self, content: str, metadata: Dict[str, Any]) -> None:
        """Chunk document, generate embeddings, and store in JSON database."""
        chunks = self.chunk_text(content)
        
        for i, chunk in enumerate(chunks):            
            chunk_text = chunk
            chunk_metadata = {
                **metadata,
                "chunk_index": i,
                "total_chunks": len(chunks),
            }            
            
            embedding = self.embed(chunk_text)
            
            # Create document entry
            doc = {
                "id": f"{metadata['filename']}_{i}",
                "content": chunk_text,
                "embedding": embedding,
                "metadata": chunk_metadata
            }
            
            # Add to document store
            self.documents.append(doc)
        
        # Save updated documents
        self._save_documents()


  def embed(self, text: str) -> List[float]:
    embeddings = embed_texts([text], 'document')['embeddings']
    return embeddings[0]
  
  def embed_query(self, query: str) -> List[float]:
    embeddings = embed_texts([query], 'query')['embeddings']
    return embeddings[0]