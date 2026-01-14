"""
Test script for RAG API
Run after starting server: uvicorn main:app --reload
"""

import requests
import json

BASE = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health ===")
    r = requests.get(f"{BASE}/health")
    print(f"Status: {r.status_code}")
    print(f"Response: {json.dumps(r.json(), indent=2)}")

def create_test_file():
    """Create sample text file"""
    content = """
    Machine Learning Basics
    
    Machine learning is a branch of artificial intelligence that enables 
    computers to learn from data. It uses statistical methods to identify 
    patterns and make predictions.
    
    Deep learning is a subset of machine learning that uses neural networks 
    with multiple layers. It's particularly effective for image recognition 
    and natural language processing tasks.
    """
    
    with open('test_doc.txt', 'w') as f:
        f.write(content)
    
    print("\n✓ Created test_doc.txt")
    return 'test_doc.txt'

def test_upload(filepath):
    """Test upload endpoint"""
    print("\n=== Testing Upload ===")
    
    with open(filepath, 'rb') as f:
        files = {'file': f}
        r = requests.post(f"{BASE}/upload", files=files)
    
    print(f"Status: {r.status_code}")
    print(f"Response: {json.dumps(r.json(), indent=2)}")
    
    if r.status_code == 200:
        return r.json()['document_id']
    return None

def test_query(question):
    """Test query endpoint"""
    print(f"\n=== Testing Query: {question} ===")
    
    data = {"question": question, "top_k": 3}
    r = requests.post(f"{BASE}/query", json=data)
    
    print(f"Status: {r.status_code}")
    print(f"Response: {json.dumps(r.json(), indent=2)}")

def test_list():
    """Test list documents"""
    print("\n=== Testing List Documents ===")
    r = requests.get(f"{BASE}/documents")
    print(f"Status: {r.status_code}")
    print(f"Response: {json.dumps(r.json(), indent=2)}")

if __name__ == "__main__":
    print("="*50)
    print("RAG API Test Suite")
    print("="*50)
    
    try:
        # test health
        test_health()
        
        # create and upload file
        file = create_test_file()
        doc_id = test_upload(file)
        
        if doc_id:
            # test queries
            test_query("What is machine learning?")
            test_query("Explain deep learning")
            
            # list documents
            test_list()
        
        print("\n" + "="*50)
        print("Testing Complete!")
        print("="*50)
        
    except requests.exceptions.ConnectionError:
        print("\n Error: Server not running!")
        print("Start server: uvicorn main:app --reload")
    except Exception as e:
        print(f"\n Error: {e}")