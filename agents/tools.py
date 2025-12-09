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
        self.reports_dir = base_dir / 'reports'
        
        # Ensure directories exist
        self.generated_code_dir.mkdir(exist_ok=True)
        self.raw_text_dir.mkdir(exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)
    
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
    
    def calculate_detailed_statistics(self, csv_path: str) -> dict:
        """
        Calculate detailed statistics for all columns in CSV.
        
        Args:
            csv_path: Path to the CSV file
        
        Returns:
            dict with comprehensive statistics
        """
        try:
            df = pd.read_csv(csv_path)
            
            stats_report = {
                'numeric_columns': {},
                'categorical_columns': {},
                'overall': {
                    'total_rows': int(len(df)),
                    'total_columns': int(len(df.columns)),
                    'memory_usage': int(df.memory_usage(deep=True).sum())
                }
            }
            
            # Numeric column statistics
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            for col in numeric_cols:
                stats_report['numeric_columns'][col] = {
                    'count': int(df[col].count()),
                    'mean': float(df[col].mean()) if not pd.isna(df[col].mean()) else 0.0,
                    'std': float(df[col].std()) if not pd.isna(df[col].std()) else 0.0,
                    'min': float(df[col].min()) if not pd.isna(df[col].min()) else 0.0,
                    'max': float(df[col].max()) if not pd.isna(df[col].max()) else 0.0,
                    '25%': float(df[col].quantile(0.25)) if not pd.isna(df[col].quantile(0.25)) else 0.0,
                    '50%': float(df[col].quantile(0.50)) if not pd.isna(df[col].quantile(0.50)) else 0.0,
                    '75%': float(df[col].quantile(0.75)) if not pd.isna(df[col].quantile(0.75)) else 0.0,
                    'missing': int(df[col].isnull().sum())
                }
            
            # Categorical column statistics
            categorical_cols = df.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                value_counts = df[col].value_counts().head(10).to_dict()
                stats_report['categorical_columns'][col] = {
                    'count': int(df[col].count()),
                    'unique': int(df[col].nunique()),
                    'top_values': {str(k): int(v) for k, v in value_counts.items()},
                    'missing': int(df[col].isnull().sum())
                }
            
            return {
                'status': 'success',
                'statistics': stats_report
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error calculating statistics: {str(e)}'
            }
    
    def check_data_quality(self, csv_path: str) -> dict:
        """
        Perform data quality checks on CSV file.
        
        Args:
            csv_path: Path to the CSV file
        
        Returns:
            dict with quality check results
        """
        try:
            df = pd.read_csv(csv_path)
            
            quality_report = {
                'missing_values': {},
                'duplicates': {
                    'total_duplicates': int(df.duplicated().sum()),
                    'duplicate_percentage': float((df.duplicated().sum() / len(df)) * 100)
                },
                'outliers': {},
                'data_types': {}
            }
            
            # Missing values analysis
            for col in df.columns:
                missing_count = int(df[col].isnull().sum())
                if missing_count > 0:
                    quality_report['missing_values'][col] = {
                        'count': missing_count,
                        'percentage': float((missing_count / len(df)) * 100)
                    }
            
            # Outlier detection for numeric columns (using IQR method)
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            for col in numeric_cols:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = df[(df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))]
                
                if len(outliers) > 0:
                    quality_report['outliers'][col] = {
                        'count': int(len(outliers)),
                        'percentage': float((len(outliers) / len(df)) * 100)
                    }
            
            # Data type information
            for col in df.columns:
                quality_report['data_types'][col] = str(df[col].dtype)
            
            return {
                'status': 'success',
                'quality_report': quality_report
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error checking data quality: {str(e)}'
            }
    
    def generate_csv_report(self, csv_path: str, stats: dict, quality: dict) -> dict:
        """
        Generate an HTML report with statistics and quality checks.
        
        Args:
            csv_path: Path to the CSV file
            stats: Statistics dictionary
            quality: Quality report dictionary
        
        Returns:
            dict with report file path
        """
        try:
            csv_name = Path(csv_path).stem
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_filename = f"{csv_name}_report_{timestamp}.html"
            report_path = self.reports_dir / report_filename
            
            # Create HTML report
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>CSV Analysis Report - {csv_name}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                    .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                    h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
                    h2 {{ color: #555; margin-top: 30px; border-bottom: 2px solid #ddd; padding-bottom: 8px; }}
                    h3 {{ color: #666; }}
                    table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
                    th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                    th {{ background-color: #4CAF50; color: white; }}
                    tr:nth-child(even) {{ background-color: #f9f9f9; }}
                    .metric {{ display: inline-block; margin: 10px 20px 10px 0; padding: 15px; background: #e8f5e9; border-radius: 5px; }}
                    .metric-label {{ font-weight: bold; color: #2e7d32; }}
                    .metric-value {{ font-size: 24px; color: #1b5e20; }}
                    .warning {{ background-color: #fff3cd; padding: 10px; border-left: 4px solid #ffc107; margin: 10px 0; }}
                    .info {{ background-color: #d1ecf1; padding: 10px; border-left: 4px solid #17a2b8; margin: 10px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>📊 CSV Analysis Report</h1>
                    <p><strong>File:</strong> {csv_name}</p>
                    <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    
                    <h2>Overall Statistics</h2>
                    <div class="metric">
                        <div class="metric-label">Total Rows</div>
                        <div class="metric-value">{stats.get('overall', {}).get('total_rows', 'N/A')}</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Total Columns</div>
                        <div class="metric-value">{stats.get('overall', {}).get('total_columns', 'N/A')}</div>
                    </div>
                    
                    <h2>Numeric Columns Statistics</h2>
            """
            
            # Add numeric statistics table
            if stats.get('numeric_columns'):
                html_content += "<table><tr><th>Column</th><th>Mean</th><th>Std</th><th>Min</th><th>Max</th><th>Missing</th></tr>"
                for col, col_stats in stats['numeric_columns'].items():
                    html_content += f"""
                    <tr>
                        <td><strong>{col}</strong></td>
                        <td>{col_stats.get('mean', 0):.2f}</td>
                        <td>{col_stats.get('std', 0):.2f}</td>
                        <td>{col_stats.get('min', 0):.2f}</td>
                        <td>{col_stats.get('max', 0):.2f}</td>
                        <td>{col_stats.get('missing', 0)}</td>
                    </tr>
                    """
                html_content += "</table>"
            
            # Add categorical statistics
            if stats.get('categorical_columns'):
                html_content += "<h2>Categorical Columns</h2><table><tr><th>Column</th><th>Unique Values</th><th>Missing</th></tr>"
                for col, col_stats in stats['categorical_columns'].items():
                    html_content += f"""
                    <tr>
                        <td><strong>{col}</strong></td>
                        <td>{col_stats.get('unique', 0)}</td>
                        <td>{col_stats.get('missing', 0)}</td>
                    </tr>
                    """
                html_content += "</table>"
            
            # Add quality report
            html_content += "<h2>Data Quality Report</h2>"
            
            if quality.get('missing_values'):
                html_content += '<div class="warning"><strong>⚠ Missing Values Detected</strong><ul>'
                for col, info in quality['missing_values'].items():
                    html_content += f"<li><strong>{col}</strong>: {info['count']} missing ({info['percentage']:.2f}%)</li>"
                html_content += "</ul></div>"
            
            if quality.get('duplicates', {}).get('total_duplicates', 0) > 0:
                html_content += f'<div class="warning"><strong>⚠ Duplicate Rows</strong><p>{quality["duplicates"]["total_duplicates"]} duplicate rows found ({quality["duplicates"]["duplicate_percentage"]:.2f}%)</p></div>'
            
            if quality.get('outliers'):
                html_content += '<div class="info"><strong>ℹ Outliers Detected</strong><ul>'
                for col, info in quality['outliers'].items():
                    html_content += f"<li><strong>{col}</strong>: {info['count']} outliers ({info['percentage']:.2f}%)</li>"
                html_content += "</ul></div>"
            
            html_content += """
                </div>
            </body>
            </html>
            """
            
            # Save report
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return {
                'status': 'success',
                'report_path': str(report_path),
                'report_filename': report_filename
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error generating report: {str(e)}'
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
