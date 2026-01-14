# Document Q&A System - RAG Implementation

**AI Engineer Assignment - Task 1**

A backend API service for uploading documents and asking questions using Retrieval-Augmented Generation (RAG).

---

## Project Overview

**Selected Task:** Task 1 - Document Q&A Microservice (RAG)

This system implements a complete RAG pipeline:

1. Upload PDF/TXT documents
2. Extract and chunk text
3. Generate embeddings using sentence-transformers
4. Store in ChromaDB (vector database)
5. Store metadata in SQLite
6. Answer questions using retrieved context and LLM

---

## Architecture Summary

```
User Request
     ↓
FastAPI Server (main.py)
     ↓
┌────────────────┬──────────────┬────────────┬──────────┐
│                │              │            │          │
Document      Vector        Database      LLM      Uploads
Processor     Store         (SQLite)    Handler    Folder
     ↓            ↓              ↓           ↓
Extract &    Embeddings    Metadata    Groq/OpenAI
Chunk       + ChromaDB     Storage        API
```

**Components:**

- `main.py` - FastAPI endpoints
- `document_processor.py` - Text extraction and chunking
- `vector_store.py` - Embeddings and ChromaDB
- `database.py` - SQLite metadata storage
- `llm_handler.py` - LLM integration

---

## Tech Stack

- **Framework:** FastAPI
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB:** ChromaDB
- **Database:** SQLite
- **LLM:** Groq API / OpenAI
- **PDF Processing:** PyPDF2
- **Python:** 3.8+

---

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (venv)

### Installation (Windows - Easiest)

**Step 1: Run Setup Script**

Simply double-click `setup.bat` or run in Command Prompt:

```bash
setup.bat
```

This will automatically:
- Create virtual environment
- Install all dependencies
- Create configuration file (.env)
- Create uploads folder
- **Start the server**

Then open your browser to: **http://127.0.0.1:8000/docs**

---

### Installation (Linux/macOS)

**Step 1: Run Setup Script**

```bash
chmod +x setup.sh
./setup.sh
```

This will automatically:
- Create virtual environment
- Install all dependencies
- Create configuration file (.env)
- Create uploads folder
- **Start the server**

Then open your browser to: **http://127.0.0.1:8000/docs**

---

### Manual Installation (If scripts don't work)

**Step 1: Create Virtual Environment**

```bash
python -m venv venv
```

**Step 2: Activate Virtual Environment**

Windows:
```bash
.\venv\Scripts\Activate.ps1
```

Linux/macOS:
```bash
source venv/bin/activate
```

**Step 3: Install Dependencies**

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

**Step 4: Configure Environment**

Create a `.env` file in the project root:

```env
# Groq API Configuration
# Get your API key from https://console.groq.com
GROQ_API_KEY=your_groq_api_key_here

# Server Configuration
SERVER_HOST=127.0.0.1
SERVER_PORT=8000

# Database Configuration
DATABASE_PATH=documents.db

# Vector Store Configuration
VECTOR_DB_PATH=./chroma_db

# Chunk Configuration
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

**Step 5: Create Uploads Folder**

```bash
mkdir uploads
```

**Step 6: Start Server**

```bash
python main.py
```

Server runs at: **http://127.0.0.1:8000**

Interactive Docs: **http://127.0.0.1:8000/docs**

---

## Quick Start

1. **Upload a document:**
   - Go to http://127.0.0.1:8000/docs
   - Click on `/upload` endpoint
   - Select a PDF or TXT file
   - Click "Try it out"

2. **Ask a question:**
   - In the same Swagger UI
   - Go to `/query` endpoint
   - Enter your question
   - Get instant answers

3. **View all documents:**
   - Use `/documents` endpoint to list uploads

---

## API Endpoints

### 1. Health Check

```bash
GET /health
```

Example:
```bash
curl http://127.0.0.1:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-14T12:00:00"
}
```

### 2. Upload Document

```bash
POST /upload
```

Upload PDF or TXT file and automatically extract, chunk, and embed.

**Example with cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/upload" \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "message": "Document uploaded successfully",
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "document.pdf",
  "chunks": 25,
  "upload_time": "2026-01-14T12:00:00"
}
```

### 3. Query Documents

```bash
POST /query
```

Ask questions about uploaded documents with RAG.

**Request:**
```json
{
  "question": "What is machine learning?",
  "document_id": null,
  "top_k": 3
}
```

**Example with cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main topic?",
    "top_k": 3
  }'
```

**Response:**
```json
{
  "answer": "Based on the document: Machine learning is...",
  "sources": [
    {
      "rank": 1,
      "text": "Machine learning enables computers to learn...",
      "score": 0.892
    },
    {
      "rank": 2,
      "text": "Deep learning uses neural networks...",
      "score": 0.856
    }
  ]
}
```

### 4. List All Documents

```bash
GET /documents
```

Get list of all uploaded documents.

**Example:**
```bash
curl http://127.0.0.1:8000/documents
```

**Response:**
```json
{
  "count": 2,
  "documents": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "filename": "document1.pdf",
      "upload_time": "2026-01-14T12:00:00",
      "num_chunks": 25
    }
  ]
}
```

### 5. Delete Document

```bash
DELETE /documents/{document_id}
```

Remove a document and all its embeddings.

**Example:**
```bash
curl -X DELETE "http://127.0.0.1:8000/documents/550e8400-e29b-41d4-a716-446655440000"
```

**Response:**
```json
{
  "message": "Document deleted",
  "id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

## Testing

### Method 1: Interactive API Docs (Recommended)

1. Start the server:
   ```bash
   python main.py
   ```
2. Open browser: http://127.0.0.1:8000/docs
3. Test all endpoints interactively in Swagger UI

**Features:**
- Try out endpoints
- See request/response examples
- Download curl commands

### Method 2: Swagger UI Alternative

Open: http://127.0.0.1:8000/redoc

### Method 3: cURL Command Line

```bash
# Upload document
curl -X POST "http://127.0.0.1:8000/upload" \
  -F "file=@sample.txt"

# Ask a question
curl -X POST "http://127.0.0.1:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?"}'

# List documents
curl http://127.0.0.1:8000/documents

# Check health
curl http://127.0.0.1:8000/health
```

### Method 4: Python Script

```python
import requests

BASE = "http://127.0.0.1:8000"

# Upload document
with open('sample.txt', 'rb') as f:
    files = {'file': f}
    response = requests.post(f"{BASE}/upload", files=files)
    doc_id = response.json()['document_id']
    print(f"Uploaded: {doc_id}")

# Query document
query_data = {
    "question": "What is the main topic?",
    "top_k": 3
}
response = requests.post(f"{BASE}/query", json=query_data)
print(response.json()['answer'])

# Get all documents
response = requests.get(f"{BASE}/documents")
print(response.json())

# Delete document
requests.delete(f"{BASE}/documents/{doc_id}")
```

### Test with Sample File

A sample text file is included in `uploads/ai_basics.txt`. Try uploading and querying it!

---

## Project Structure

```
document-qa-rag/
├── main.py                  # FastAPI app
├── document_processor.py    # Text extraction
├── vector_store.py          # Embeddings & ChromaDB
├── database.py              # SQLite operations
├── llm_handler.py           # LLM integration
├── requirements.txt         # Dependencies
├── setup.sh                 # Setup script
├── README.md                # This file
├── .gitignore               # Git ignore
├── uploads/                 # Uploaded files
└── documents.db             # SQLite database
```

---

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GROQ_API_KEY` | Groq API key for LLM | None | No |
| `SERVER_HOST` | Server host address | 127.0.0.1 | No |
| `SERVER_PORT` | Server port number | 8000 | No |
| `DATABASE_PATH` | SQLite database path | documents.db | No |
| `VECTOR_DB_PATH` | ChromaDB path | ./chroma_db | No |
| `CHUNK_SIZE` | Text chunk size | 500 | No |
| `CHUNK_OVERLAP` | Chunk overlap | 50 | No |

**How to set variables:**

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY = "your-api-key"
```

**Windows (CMD):**
```cmd
set GROQ_API_KEY=your-api-key
```

**Linux/Mac:**
```bash
export GROQ_API_KEY="your-api-key"
```

Or use `.env` file in project root (easier).

---

## Configuration

### .env File Example

```env
# Get free API key from https://console.groq.com
GROQ_API_KEY=PUT_HERE_APT_KEY

# Server settings
SERVER_HOST=127.0.0.1
SERVER_PORT=8000

# Database
DATABASE_PATH=documents.db
VECTOR_DB_PATH=./chroma_db

# Text processing
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

### Without Groq API Key

The system works without an API key! You'll get:
- Document upload ✓
- Text chunking ✓
- Embedding generation ✓
- Similarity search ✓
- Basic text preview as answer (no LLM)

To get better answers, add your free Groq API key to `.env`

---

## Notes and Assumptions

### Design Decisions

**Chunking:**
- Size: 500 characters
- Overlap: 50 characters
- Reason: Balance between context and granularity

**Embeddings:**
- Model: all-MiniLM-L6-v2
- Reason: Fast, accurate, runs locally

**Vector DB:**
- ChromaDB (in-memory)
- Reason: Simple, no server needed

**SQL DB:**
- SQLite
- Reason: Lightweight, portable

**LLM:**
- Groq (primary) - fast, free tier
- OpenAI (fallback)
- Simple context return (no API)

### Assumptions

- Text-based PDFs (not scanned images)
- Single-user environment
- English language
- Files under 10MB

### Limitations

- ChromaDB in-memory (data lost on restart)
- No authentication
- Single file upload at a time
- No OCR support

---

## Troubleshooting

### Server Issues

**"Address already in use"**
```bash
# Change port in main.py or use:
uvicorn main:app --port 8001
```

**"Connection refused"**
- Ensure server is running: `python main.py`
- Check if using correct URL: http://127.0.0.1:8000
- Verify port 8000 is not blocked by firewall

**"ModuleNotFoundError"**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Document Upload Issues

**"File not found"**
- Ensure file exists in current directory
- Use full path: `C:\path\to\file.pdf`

**"No text found in document"**
- PDF might be scanned image (need OCR)
- Try converting to TXT first
- Check if PDF is corrupted

**"File too large"**
- Recommended max: 10MB
- Split large documents first

### Query Issues

**"No relevant information found"**
- Document might not contain the answer
- Try different wording in question
- Check if document was uploaded successfully

**"Slow first query (5-10 seconds)"**
- Normal! Embedding model loads on first use
- Subsequent queries are faster
- Model is cached after first load

**"Empty or generic answers**
- Add Groq API key to `.env` for better LLM answers
- Without API key, gets basic text preview

### ChromaDB Issues

```bash
# Clear ChromaDB cache
rm -rf chroma_db
```

Then restart server - it will recreate the database.

### Python Version Issues

**Python 3.13 working:**
- Successfully tested with Python 3.13.7
- Pre-built wheels for numpy and torch available
- No compilation issues

**Python 3.8-3.12 also supported**

### Performance Tips

1. **Faster uploads:**
   - Smaller text files
   - Pre-chunked documents

2. **Faster queries:**
   - Reduce `top_k` parameter
   - Use specific questions

3. **Lower memory usage:**
   - Reduce `CHUNK_SIZE`
   - Delete unused documents

---

## Sample Test Documents

Free PDFs for testing:

1. Attention Is All You Need (Transformer paper)
2. Python Data Science Handbook
3. Any technical documentation

---

## Development

### Running in Development Mode

```bash
# With auto-reload and debug logging
uvicorn main:app --reload --log-level debug

# Or using Python directly
python main.py
```

### Code Structure Overview

**main.py** - FastAPI application
- `/health` - Health check endpoint
- `/upload` - File upload with processing
- `/query` - Question answering endpoint
- `/documents` - List/delete documents

**document_processor.py** - Text processing
- PDF/TXT extraction
- Text chunking with overlap
- Text cleaning and normalization

**vector_store.py** - Vector operations
- Embedding generation (sentence-transformers)
- ChromaDB vector storage
- Similarity search

**database.py** - Metadata storage
- SQLite for document metadata
- Chunk tracking
- Document retrieval

**llm_handler.py** - LLM integration
- Groq API calls (primary)
- Fallback text preview
- Answer generation

### Adding Features

To add new endpoints:
1. Add route to `main.py`
2. Update API docs in README
3. Test with Swagger UI

To change embedding model:
1. Edit `vector_store.py` line 14
2. Replace model name: `SentenceTransformer('all-MiniLM-L6-v2')`

To change chunk size:
1. Edit `.env` file
2. Or modify `main.py` initialization

---

---

## What's Included

### Files in This Project

-  `main.py` - FastAPI server with 5 endpoints
-  `document_processor.py` - PDF/TXT extraction & chunking
-  `vector_store.py` - Embeddings & ChromaDB integration
-  `database.py` - SQLite metadata storage
-  `llm_handler.py` - Groq LLM integration (fixed)
-  `.env` - Configuration file (created)
-  `requirements.txt` - All dependencies
-  `venv/` - Virtual environment
-  `uploads/` - Document storage
-  `documents.db` - SQLite database (auto-created)

### What Works

-  Server runs on http://127.0.0.1:8000
-  Swagger UI at /docs
-  Upload PDF/TXT documents
-  Automatic text extraction & chunking
-  Embedding generation (local, no API needed)
-  Vector similarity search
-  Question answering with retrieved context
-  Metadata storage in SQLite
-  Document management (list/delete)

### Fixes Applied

-  Fixed `llm_handler.py` API key configuration
-  Corrected Groq API endpoint URL
-  Updated host to 127.0.0.1 (localhost)
- Created `.env` configuration file
-  Fixed requirements.txt for Windows compatibility
-  All dependencies installed successfully

---

## System Requirements

- **OS:** Windows, macOS, Linux
- **Python:** 3.8+ (tested on 3.13.7)
- **RAM:** 4GB minimum (8GB recommended)
- **Disk:** 2GB for models & databases
- **Network:** For downloading pre-trained embeddings (one-time)

---

## Getting Started (TL;DR)

**Windows Users:** Just double-click `setup.bat` and wait!

**Linux/macOS Users:**
```bash
chmod +x setup.sh
./setup.sh
```

That's it! The script will:
1.  Create virtual environment
2.  Install all dependencies
3.  Configure settings
4.  Start the server

Then open: **http://127.0.0.1:8000/docs**

---



---

**Author:** [SANJAY KUMAR SHUKLA]  
**Date:** January 2026  
**Task:** Task 1 - Document Q&A RAG System

