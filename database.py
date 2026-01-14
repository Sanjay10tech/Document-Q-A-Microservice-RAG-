import sqlite3
import json
import uuid

class Database:
    """Store document metadata in SQLite"""
    
    def __init__(self, db_path="documents.db"):
        self.db_path = db_path
        self._create_tables()
    
    def _create_tables(self):
        """Create documents table if not exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                upload_time TEXT NOT NULL,
                chunk_ids TEXT NOT NULL,
                num_chunks INTEGER NOT NULL,
                file_path TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_document(self, metadata):
        """Save document metadata and return document ID"""
        doc_id = str(uuid.uuid4())
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO documents (id, filename, upload_time, chunk_ids, num_chunks, file_path)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            doc_id,
            metadata['filename'],
            metadata['upload_time'],
            json.dumps(metadata['chunk_ids']),
            metadata['num_chunks'],
            metadata['file_path']
        ))
        
        conn.commit()
        conn.close()
        
        return doc_id
    
    def get_document(self, doc_id):
        """Get document metadata by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, filename, upload_time, chunk_ids, num_chunks, file_path
            FROM documents
            WHERE id = ?
        ''', (doc_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "filename": row[1],
                "upload_time": row[2],
                "chunk_ids": json.loads(row[3]),
                "num_chunks": row[4],
                "file_path": row[5]
            }
        
        return None
    
    def get_all_documents(self):
        """Get all documents"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, filename, upload_time, num_chunks
            FROM documents
            ORDER BY upload_time DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        documents = []
        for row in rows:
            documents.append({
                "id": row[0],
                "filename": row[1],
                "upload_time": row[2],
                "num_chunks": row[3]
            })
        
        return documents
    
    def delete_document(self, doc_id):
        """Delete document from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM documents WHERE id = ?', (doc_id,))
        
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return deleted