import PyPDF2
import re

class DocumentProcessor:
    """Extract text from documents and split into chunks"""
    
    def __init__(self, chunk_size=500, overlap=50):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def extract_text(self, filepath):
        """Extract text from PDF or TXT file"""
        if filepath.endswith('.pdf'):
            return self._extract_pdf(filepath)
        elif filepath.endswith('.txt'):
            return self._extract_txt(filepath)
        else:
            raise ValueError("Unsupported file type")
    
    def _extract_pdf(self, filepath):
        """Read PDF and extract all text"""
        text = ""
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                for page_num in range(total_pages):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    
                    if page_text:
                        text += page_text + "\n"
            
            return text
            
        except Exception as e:
            raise Exception(f"PDF extraction error: {str(e)}")
    
    def _extract_txt(self, filepath):
        """Read text file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"TXT extraction error: {str(e)}")
    
    def chunk_text(self, text):
        """Split text into overlapping chunks"""
        cleaned = self._clean_text(text)
        sentences = self._split_sentences(cleaned)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) > self.chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                if len(current_chunk) > self.overlap:
                    overlap_text = current_chunk[-self.overlap:]
                else:
                    overlap_text = current_chunk
                
                current_chunk = overlap_text + " " + sentence
            else:
                current_chunk += " " + sentence
        
        # add last chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _clean_text(self, text):
        """Remove whitespace and special characters"""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,!?;:(\)\-]', '', text)
        
        return text.strip()
    
    def _split_sentences(self, text):
        """Split text into sentences"""
        # simple sentence splitter based on punctuation
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # filter empty sentences
        return [s.strip() for s in sentences if s.strip()]