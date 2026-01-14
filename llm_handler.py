import os
import requests
from dotenv import load_dotenv
load_dotenv()

class LLMHandler:
    """Generate answers using Groq API"""
    
    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
       
    
    def generate_answer(self, question, context):
        """Generate answer from context using Groq API or fallback"""
        if self.groq_key:
            try:
                return self._groq_answer(question, context)
            except Exception as e:
                print(f"Groq API failed: {e}")
        
        return self._simple_answer(context)
    
    def _groq_answer(self, question, context):
        """Call Groq API"""
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.groq_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""Answer the question based on the context below.

Context:
{context}

Question: {question}

Answer:"""
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Answer questions based only on the given context."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": 500
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        answer = result['choices'][0]['message']['content'].strip()
        
        return answer
    
   
    
    def _simple_answer(self, context):
        """Return document preview when API unavailable"""
        preview = context[:300]
        return f"Based on the document: {preview}"