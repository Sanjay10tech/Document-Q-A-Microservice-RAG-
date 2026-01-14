from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime
import os
import shutil

from document_processor import DocumentProcessor
from vector_store import VectorStore
from database import Database
from llm_handler import LLMHandler

app = FastAPI(
    title="Document Q&A RAG System",
    description="Upload documents and ask questions - Task 1 Assignment"
)

print("Starting RAG system...")
doc_processor = DocumentProcessor()
vector_db = VectorStore()
metadata_db = Database()
llm = LLMHandler()
print("System initialized successfully!\n")
class QueryRequest(BaseModel):
    question: str
    document_id: Optional[str] = None
    top_k: int = 3

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]

@app.get("/")
def root():
    """API information"""
    return {
        "message": "Document Q&A RAG System",
        "version": "1.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health():
    """Check if system is running"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/upload")
async def upload_doc(file: UploadFile = File(...)):
    """Upload PDF or TXT file and process for Q&A"""
    try:
        print(f"\n--- Uploading: {file.filename} ---")
        
        if not file.filename.endswith(('.pdf', '.txt')):
            raise HTTPException(400, "Only PDF and TXT files supported")
        
        os.makedirs("uploads", exist_ok=True)
        filepath = f"uploads/{file.filename}"
        with open(filepath, "wb") as f:
            shutil.copyfileobj(file.file, f)
        print(f"File saved: {filepath}")
        
        print("Extracting text...")
        text = doc_processor.extract_text(filepath)
        if not text or len(text.strip()) == 0:
            raise HTTPException(400, "No text found in document")
        print(f"Extracted {len(text)} characters")
        
        print("Chunking text...")
        chunks = doc_processor.chunk_text(text)
        print(f"Created {len(chunks)} chunks")
        
        print("Generating embeddings...")
        embeddings = vector_db.create_embeddings(chunks)
        
        print("Saving to vector database...")
        chunk_ids = vector_db.store_chunks(
            embeddings=embeddings,
            texts=chunks,
            metadata={"filename": file.filename}
        )
        
        doc_metadata = {
            "filename": file.filename,
            "upload_time": datetime.now().isoformat(),
            "chunk_ids": chunk_ids,
            "num_chunks": len(chunks),
            "file_path": filepath
        }
        
        doc_id = metadata_db.save_document(doc_metadata)
        
        print(f"Document ID: {doc_id}")
        print("--- Upload complete ---\n")
        
        return {
            "message": "Document uploaded successfully",
            "document_id": doc_id,
            "filename": file.filename,
            "chunks": len(chunks),
            "upload_time": doc_metadata["upload_time"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(500, f"Upload failed: {str(e)}")

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Search documents and generate answers using RAG"""
    try:
        print(f"\n--- Query: {request.question} ---")
        
        print("Creating query embedding...")
        query_emb = vector_db.create_embeddings([request.question])[0]
        
        print(f"Searching top {request.top_k} chunks...")
        results = vector_db.search_similar(query_emb, top_k=request.top_k)
        
        if not results:
            return QueryResponse(
                answer="No relevant information found in documents.",
                sources=[]
            )
        
        print(f"Found {len(results)} relevant chunks")
        
        # prepare context
        context = "\n\n".join([r["text"] for r in results])
        
        # generate answer
        print("Generating answer...")
        answer = llm.generate_answer(request.question, context)
        
        # prepare sources
        sources = []
        for i, r in enumerate(results):
            text_preview = r["text"][:150] + "..." if len(r["text"]) > 150 else r["text"]
            sources.append({
                "rank": i + 1,
                "text": text_preview,
                "score": round(r["score"], 3)
            })
        
        print("--- Query complete ---\n")
        
        return QueryResponse(answer=answer, sources=sources)
        
    except Exception as e:
        print(f"Query error: {e}")
        raise HTTPException(500, f"Query failed: {str(e)}")

@app.get("/documents")
def list_docs():
    """Get all uploaded documents"""
    try:
        docs = metadata_db.get_all_documents()
        return {
            "count": len(docs),
            "documents": docs
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@app.delete("/documents/{doc_id}")
def delete_doc(doc_id: str):
    """Delete a document"""
    try:
        # get document info
        doc = metadata_db.get_document(doc_id)
        
        if not doc:
            raise HTTPException(404, "Document not found")
        
        # delete from vector db
        vector_db.delete_chunks(doc["chunk_ids"])
        
        # delete from metadata db
        metadata_db.delete_document(doc_id)
        
        # delete file
        if os.path.exists(doc["file_path"]):
            os.remove(doc["file_path"])
        
        return {"message": "Document deleted", "id": doc_id}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)