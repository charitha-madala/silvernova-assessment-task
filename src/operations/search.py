from typing import Dict, Any, List
from src.operations.embed import EmbedService

class SearchEngine:
  
  def __init__(self) -> None:
    self.embed = EmbedService('embedded_doc.json')
    self.documents = self.embed.documents  
  
  def search_similar(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Find documents similar to the query."""
        
        query_embedding = self.embed.embed_query(query)
        
        results = []
        
        for doc in self.documents:
            doc_embedding = doc["embedding"]
            
            # dot product
            dot_product = sum(q * d for q, d in zip(query_embedding, doc_embedding))
            
            #  magnitudes
            query_magnitude = (sum(q * q for q in query_embedding)) ** 0.5
            doc_magnitude = (sum(d * d for d in doc_embedding)) ** 0.5
            
            #  cosine similarity
            similarity = dot_product / (query_magnitude * doc_magnitude) if query_magnitude and doc_magnitude else 0            

            results.append({
                "id": doc["id"],
                "content": doc["content"],
                "metadata": doc["metadata"],
                "score": float(similarity)
            })
        
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results[:limit]