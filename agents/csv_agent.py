"""
CSV Analysis Agent with human-in-the-loop suggestions using Groq API.
"""
from groq import Groq
from .tools import FileSystemTools
import json
from pathlib import Path


class CSVAnalysisAgent:
    """Agent that analyzes CSV files and provides intelligent suggestions."""
    
    def __init__(self, api_key: str, fs_tools: FileSystemTools):
        self.client = Groq(api_key=api_key)
        self.fs_tools = fs_tools
        self.model_id = "llama-3.3-70b-versatile"
    
    def analyze_csv(self, csv_path: str) -> dict:
        """
        Analyze CSV file and provide intelligent suggestions.
        
        Args:
            csv_path: Path to the CSV file
        
        Returns:
            dict with analysis, content summary, and actionable suggestions
        """
        try:
            # Get CSV structure analysis
            analysis = self.fs_tools.analyze_csv_structure(csv_path)
            
            if analysis['status'] != 'success':
                return analysis
            
            # Generate content summary and suggestions using Groq
            summary_and_suggestions = self._generate_summary_and_suggestions(analysis)
            
            return {
                'status': 'success',
                'filename': Path(csv_path).name,
                'num_rows': analysis['num_rows'],
                'num_cols': analysis['num_cols'],
                'columns': analysis['columns'],
                'content_summary': summary_and_suggestions['content_summary'],
                'suggestions': summary_and_suggestions['suggestions'],
                'sample_data': analysis['sample_data'][:3],  # Show first 3 rows
                'message': 'CSV analyzed successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error analyzing CSV: {str(e)}'
            }
    
    def _generate_summary_and_suggestions(self, analysis: dict) -> dict:
        """Generate intelligent summary and suggestions using Groq."""
        try:
            # Prepare analysis data for Groq
            columns_info = ', '.join(analysis['columns'])
            sample_data = json.dumps(analysis['sample_data'][:3], indent=2)
            
            prompt = f"""You are a data analysis expert. Analyze this CSV file and provide insights.

CSV DETAILS:
- Rows: {analysis['num_rows']}
- Columns: {analysis['num_cols']}
- Column Names: {columns_info}

SAMPLE DATA (first 3 rows):
{sample_data}

Provide:
1. A brief 1-2 sentence summary describing what this CSV contains (e.g., "employee details", "sales data", "customer information")
2. Exactly 4-5 specific, actionable suggestions for what the user could do with this data

Format your response as JSON:
{{
  "content_summary": "Brief description of the CSV content",
  "suggestions": [
    {{"id": 1, "title": "Suggestion title", "description": "Brief description"}},
    {{"id": 2, "title": "Suggestion title", "description": "Brief description"}},
    ...
  ]
}}

IMPORTANT: Return ONLY valid JSON, no additional text.
"""
            
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=800
            )
            
            # Parse JSON response
            response_text = response.choices[0].message.content.strip()
            
            # Extract JSON from response (in case it has markdown code blocks)
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            result = json.loads(response_text)
            
            return result
            
        except Exception as e:
            # Fallback suggestions if AI fails
            return {
                'content_summary': f"A CSV file with {analysis['num_cols']} columns and {analysis['num_rows']} rows",
                'suggestions': [
                    {
                        'id': 1,
                        'title': 'View Statistics',
                        'description': 'Get statistical summary of numeric columns'
                    },
                    {
                        'id': 2,
                        'title': 'Check Data Quality',
                        'description': 'Identify missing values and data issues'
                    },
                    {
                        'id': 3,
                        'title': 'Export Filtered Data',
                        'description': 'Filter and export specific rows/columns'
                    },
                    {
                        'id': 4,
                        'title': 'Generate Report',
                        'description': 'Create a summary report of the data'
                    }
                ]
            }
    
    def execute_action(self, csv_path: str, action_id: int, analysis: dict) -> dict:
        """
        Execute a selected action on the CSV file.
        
        Args:
            csv_path: Path to the CSV file
            action_id: ID of the selected action
            analysis: Previous analysis result
        
        Returns:
            dict with action result
        """
        try:
            # This is a placeholder for action execution
            # In a real implementation, you would execute specific actions
            # based on the action_id
            
            return {
                'status': 'success',
                'message': f'Action {action_id} executed successfully',
                'result': 'Action execution is a placeholder. Implement specific actions as needed.'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error executing action: {str(e)}'
            }


# Standalone function for easy integration
def analyze_csv_file(api_key: str, csv_path: str, base_dir) -> dict:
    """
    Convenience function to analyze CSV.
    
    Args:
        api_key: Groq API key
        csv_path: Path to CSV file
        base_dir: Base directory for file operations
    
    Returns:
        dict with analysis and suggestions
    """
    fs_tools = FileSystemTools(base_dir)
    agent = CSVAnalysisAgent(api_key, fs_tools)
    return agent.analyze_csv(csv_path)
