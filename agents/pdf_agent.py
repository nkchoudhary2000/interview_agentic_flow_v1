"""
PDF Extraction Agent using Groq API.
"""
from groq import Groq
from .tools import FileSystemTools
from pathlib import Path


class PDFExtractionAgent:
    """Agent that extracts text from PDF files and saves to raw_text folder."""
    
    def __init__(self, api_key: str, fs_tools: FileSystemTools):
        self.client = Groq(api_key=api_key)
        self.fs_tools = fs_tools
        self.model_id = "llama-3.3-70b-versatile"
    
    def process_pdf(self, pdf_path: str) -> dict:
        """
        Extract text from PDF and save to raw_text folder.
        
        Args:
            pdf_path: Path to the PDF file
        
        Returns:
            dict with extraction status, stats, and filepath
        """
        try:
            # Extract text from PDF
            extraction_result = self.fs_tools.extract_pdf_text(pdf_path)
            
            if extraction_result['status'] != 'success':
                return extraction_result
           
            # Get extracted text
            text = extraction_result['text']
            page_count = extraction_result['page_count']
            word_count = extraction_result['word_count']
            
            # Save to raw_text folder
            original_filename = Path(pdf_path).name
            save_result = self.fs_tools.save_text_to_file(text, original_filename)
            
            # Generate a summary using Groq
            summary = self._generate_summary(text, page_count, word_count)
            
            return {
                'status': 'success',
                'text': text,
                'page_count': page_count,
                'word_count': word_count,
                'filepath': save_result.get('filepath'),
                'summary': summary,
                'message': f'Extracted {word_count} words from {page_count} pages and saved to {save_result.get("filepath")}'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error processing PDF: {str(e)}'
            }
    
    def _generate_summary(self, text: str, page_count: int, word_count: int) -> str:
        """Generate a brief summary of the extracted content using Groq."""
        try:
            # For very long texts, only analyze first ~2000 words
            text_sample = ' '.join(text.split()[:2000])
            
            summary_prompt = f"""Provide a brief 2-3 sentence summary of this document content:

{text_sample}

Focus on the main topic and purpose of the document."""
            
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": summary_prompt}],
                temperature=0.5,
                max_tokens=200
            )
            
            summary = response.choices[0].message.content.strip()
            return f"Document Summary ({page_count} pages, {word_count} words): {summary}"
            
        except Exception:
            return f"Extracted {word_count} words from {page_count} pages."


# Standalone function for easy integration
def extract_pdf_text(api_key: str, pdf_path: str, base_dir) -> dict:
    """
    Convenience function to extract PDF text.
    
    Args:
        api_key: Groq API key
        pdf_path: Path to PDF file
        base_dir: Base directory for file operations
    
    Returns:
        dict with extracted text, stats, and filepath
    """
    fs_tools = FileSystemTools(base_dir)
    agent = PDFExtractionAgent(api_key, fs_tools)
    return agent.process_pdf(pdf_path)
