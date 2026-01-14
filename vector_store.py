from sentence_transformers import SentenceTransformer
import chromadb
import uuid

class VectorStore:
    """Generate embeddings and store in vector database"""
    
    def __init__(self):
        print("Loading embedding model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.Client()
        
        try:
            self.collection = self.client.get_collection("doc_chunks")
        except:
            self.collection = self.client.create_collection("doc_chunks")
        
        print("Vector store ready")
    
    def create_embeddings(self, texts):
        """Generate embeddings for texts"""
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
    
    def store_chunks(self, embeddings, texts, metadata=None):
        """Store chunks with embeddings in ChromaDB"""
        chunk_ids = [str(uuid.uuid4()) for _ in range(len(texts))]
        
        metadatas = []
        for i, text in enumerate(texts):
            meta = {"text": text, "chunk_index": i}
            if metadata:
                meta.update(metadata)
            metadatas.append(meta)
        
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=chunk_ids
        )
        
        return chunk_ids
    
    def search_similar(self, query_embedding, top_k=3):
        """Find similar chunks for a query"""
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        formatted_results = []
        if results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "id": results['ids'][0][i],
                    "text": results['documents'][0][i],
                    "score": 1 - results['distances'][0][i],
                    "metadata": results['metadatas'][0][i] if results['metadatas'] else {}
                })
        
        return formatted_results
    
    def delete_chunks(self, chunk_ids):
        """Delete chunks by their IDs"""
        if chunk_ids and len(chunk_ids) > 0:
            self.collection.delete(ids=chunk_ids)