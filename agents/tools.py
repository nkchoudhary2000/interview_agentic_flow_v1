"""
Custom tools for ADK agents to interact with the filesystem.
"""
import os
from pathlib import Path
from datetime import datetime
from typing import Optional
import PyPDF2
import pdfplumber
import pandas as pd


class FileSystemTools:
    """Tools for file operations used by ADK agents."""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.generated_code_dir = base_dir / 'generated_code'
        self.raw_text_dir = base_dir / 'raw_text'
        
        # Ensure directories exist
        self.generated_code_dir.mkdir(exist_ok=True)
        self.raw_text_dir.mkdir(exist_ok=True)
    
    def save_code_to_file(self, code: str, filename: str, language: str = 'python') -> dict:
        """
        Save generated code to the filesystem.
        
        Args:
            code: The code content to save
            filename: Name of the file (will be sanitized)
            language: Programming language (for file extension)
        
        Returns:
            dict with status, filepath, and message
        """
        try:
            # Sanitize filename
            safe_filename = self._sanitize_filename(filename)
            
            # Add extension if not present
            extensions = {
                'python': '.py',
                'javascript': '.js',
                'java': '.java',
                'cpp': '.cpp',
                'c': '.c',
                'html': '.html',
                'css': '.css',
                'sql': '.sql',
            }
            ext = extensions.get(language.lower(), '.txt')
            if not safe_filename.endswith(ext):
                safe_filename += ext
            
            # Create full path
            filepath = self.generated_code_dir / safe_filename
            
            # Save file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            
            return {
                'status': 'success',
                'filepath': str(filepath),
                'message': f'Code saved successfully to {safe_filename}'
            }
        except Exception as e:
            return {
                'status': 'error',
                'filepath': None,
                'message': f'Error saving code: {str(e)}'
            }
    
    def extract_pdf_text(self, pdf_path: str) -> dict:
        """
        Extract text from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
        
        Returns:
            dict with status, text, page_count, and word_count
        """
        try:
            text_content = []
            page_count = 0
            
            # Try with pdfplumber first (better for complex PDFs)
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    page_count = len(pdf.pages)
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            text_content.append(text)
            except Exception:
                # Fallback to PyPDF2
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    page_count = len(pdf_reader.pages)
                    for page in pdf_reader.pages:
                        text = page.extract_text()
                        if text:
                            text_content.append(text)
            
            full_text = '\n\n'.join(text_content)
            word_count = len(full_text.split())
            
            return {
                'status': 'success',
                'text': full_text,
                'page_count': page_count,
                'word_count': word_count,
                'message': f'Extracted {word_count} words from {page_count} pages'
            }
        except Exception as e:
            return {
                'status': 'error',
                'text': '',
                'page_count': 0,
                'word_count': 0,
                'message': f'Error extracting PDF: {str(e)}'
            }
    
    def save_text_to_file(self, text: str, original_filename: str) -> dict:
        """
        Save extracted text to the raw_text folder.
        
        Args:
            text: The text content to save
            original_filename: Original filename (will create .txt version)
        
        Returns:
            dict with status, filepath, and message
        """
        try:
            # Create .txt filename
            base_name = Path(original_filename).stem
            txt_filename = f"{base_name}.txt"
            filepath = self.raw_text_dir / txt_filename
            
            # Save file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text)
            
            return {
                'status': 'success',
                'filepath': str(filepath),
                'message': f'Text saved to {txt_filename}'
            }
        except Exception as e:
            return {
                'status': 'error',
                'filepath': None,
                'message': f'Error saving text: {str(e)}'
            }
    
    def analyze_csv_structure(self, csv_path: str) -> dict:
        """
        Analyze CSV file structure and content.
        
        Args:
            csv_path: Path to the CSV file
        
        Returns:
            dict with structure analysis, summary, and sample data
        """
        try:
            # Read CSV
            df = pd.read_csv(csv_path)
            
            # Basic info
            num_rows, num_cols = df.shape
            columns = list(df.columns)
            dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}
            
            # Sample data
            sample = df.head(5).to_dict('records')
            
            # Missing values
            missing = df.isnull().sum().to_dict()
            
            # Numeric columns stats
            numeric_stats = {}
            for col in df.select_dtypes(include=['int64', 'float64']).columns:
                numeric_stats[col] = {
                    'min': float(df[col].min()),
                    'max': float(df[col].max()),
                    'mean': float(df[col].mean()),
                    'median': float(df[col].median()),
                }
            
            return {
                'status': 'success',
                'num_rows': num_rows,
                'num_cols': num_cols,
                'columns': columns,
                'dtypes': dtypes,
                'sample_data': sample,
                'missing_values': missing,
                'numeric_stats': numeric_stats,
                'message': f'Analyzed CSV with {num_rows} rows and {num_cols} columns'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error analyzing CSV: {str(e)}'
            }
    
    def read_file_content(self, filepath: str) -> dict:
        """
        Read content from a file.
        
        Args:
            filepath: Path to the file
        
        Returns:
            dict with status, content, and message
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                'status': 'success',
                'content': content,
                'message': 'File read successfully'
            }
        except Exception as e:
            return {
                'status': 'error',
                'content': '',
                'message': f'Error reading file: {str(e)}'
            }
    
    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """Sanitize filename to remove unsafe characters."""
        # Remove or replace unsafe characters
        unsafe_chars = '<>:"/\\|?*'
        for char in unsafe_chars:
            filename = filename.replace(char, '_')
        
        # Limit length
        if len(filename) > 200:
            filename = filename[:200]
        
        # Add timestamp if filename is empty
        if not filename or filename.isspace():
            filename = f"file_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return filename
