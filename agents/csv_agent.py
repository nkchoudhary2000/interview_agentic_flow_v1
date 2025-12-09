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
        from pathlib import Path
        from .logging_utils import get_logger
        
        try:
            # Initialize logger with correct base directory
            logger = get_logger(self.fs_tools.base_dir)
            
            # Get action name from suggestions
            action_name = "Unknown Action"
            suggestions = analysis.get('suggestions', [])
            for suggestion in suggestions:
                if suggestion.get('id') == action_id:
                    action_name = suggestion.get('title', 'Unknown Action')
                    break
            
            # Log action start
            logger.log_action_start(action_id, action_name, csv_path)
            
            # Route to appropriate handler based on action_id AND action_name keywords
            result = None
            
            # Try to match by action name keywords first
            action_lower = action_name.lower()
            
            # Primary routing based on action_id with keyword fallback
            if action_id == 1 or action_id == 2:
                # Action 1-2: Usually statistics/summary
                result = self._execute_statistics(csv_path, logger)
            elif action_id == 3:
                # Action 3: Usually data quality check
                result = self._execute_quality_check(csv_path, logger)
            elif action_id == 4:
                # Action 4: Usually filtering/export
                result = self._execute_filter(csv_path, logger)
            elif action_id >= 5:
                # Action 5+: Usually report generation
                result = self._execute_report(csv_path, logger)
            else:
                # Fallback to keyword matching
                if 'statistic' in action_lower or 'summary' in action_lower or 'view' in action_lower or 'calculate' in action_lower:
                    result = self._execute_statistics(csv_path, logger)
                elif 'quality' in action_lower or 'check' in action_lower or 'validate' in action_lower or 'missing' in action_lower:
                    result = self._execute_quality_check(csv_path, logger)
                elif 'filter' in action_lower or 'export' in action_lower or 'extract' in action_lower:
                    result = self._execute_filter(csv_path, logger)
                elif 'report' in action_lower or 'generate' in action_lower or 'create' in action_lower:
                    result = self._execute_report(csv_path, logger)
                else:
                    # Default to statistics if no match
                    result = self._execute_statistics(csv_path, logger)
            
            # Log result
            logger.log_action_result(action_id, result.get('status', 'unknown'), result)
            
            # Add log file path to result
            result['log_file'] = logger.get_log_file_path()
            
            return result
            
        except Exception as e:
            # Try to log the error if logger was initialized
            try:
                if 'logger' in locals():
                    logger.log_error(action_id, f"Action execution failed: {str(e)}", e)
            except:
                pass
            
            import traceback
            return {
                'status': 'error',
                'message': f'Error executing action: {str(e)}',
                'traceback': traceback.format_exc()
            }
    
    def _execute_statistics(self, csv_path: str, logger) -> dict:
        """Execute statistics calculation action."""
        try:
            logger.log_info("Calculating detailed statistics...")
            
            # Calculate statistics using tools
            stats_result = self.fs_tools.calculate_detailed_statistics(csv_path)
            
            if stats_result['status'] != 'success':
                return stats_result
            
            stats = stats_result['statistics']
            logger.log_statistics(stats)
            
            # Format output summary
            summary = self._format_statistics_summary(stats)
            
            return {
                'status': 'success',
                'action': 'Statistics Calculation',
                'summary': summary,
                'detailed_stats': stats,
                'output': summary,
                'message': 'Statistics calculated successfully'
            }
        except Exception as e:
            logger.log_error(0, f"Statistics calculation failed: {str(e)}", e)
            return {
                'status': 'error',
                'message': f'Error calculating statistics: {str(e)}'
            }
    
    def _execute_quality_check(self, csv_path: str, logger) -> dict:
        """Execute data quality check action."""
        try:
            logger.log_info("Performing data quality check...")
            
            # Check quality using tools
            quality_result = self.fs_tools.check_data_quality(csv_path)
            
            if quality_result['status'] != 'success':
                return quality_result
            
            quality_report = quality_result['quality_report']
            logger.log_quality_check(quality_report)
            
            # Format output summary
            summary = self._format_quality_summary(quality_report)
            
            return {
                'status': 'success',
                'action': 'Data Quality Check',
                'summary': summary,
                'quality_report': quality_report,
                'output': summary,
                'message': 'Data quality check completed successfully'
            }
        except Exception as e:
            logger.log_error(0, f"Quality check failed: {str(e)}", e)
            return {
                'status': 'error',
                'message': f'Error checking data quality: {str(e)}'
            }
    
    def _execute_filter(self, csv_path: str, logger) -> dict:
        """Execute data filtering/export action."""
        try:
            logger.log_info("Preparing filtered data export...")
            
            # For now, provide information about the data structure
            # In a full implementation, this would accept filter criteria
            import pandas as pd
            from pathlib import Path
            
            df = pd.read_csv(csv_path)
            
            # Example: Export first 10 rows as a sample
            csv_name = Path(csv_path).stem
            filtered_path = self.fs_tools.base_dir / 'reports' / f'{csv_name}_sample_10.csv'
            
            df.head(10).to_csv(filtered_path, index=False)
            logger.log_info(f"Exported sample to: {filtered_path}")
            
            summary = f"""Data filtering prepared. 
            
**Sample Export:**
- Exported first 10 rows to demonstrate filtering
- File: `{filtered_path.name}`
- Total rows in original: {len(df)}

**Note:** Full filtering with custom criteria can be implemented based on your requirements."""
            
            return {
                'status': 'success',
                'action': 'Data Filtering',
                'summary': summary,
                'output': summary,
                'files_created': [str(filtered_path)],
                'message': 'Data filtering completed'
            }
        except Exception as e:
            logger.log_error(0, f"Filtering failed: {str(e)}", e)
            return {
                'status': 'error',
                'message': f'Error filtering data: {str(e)}'
            }
    
    def _execute_report(self, csv_path: str, logger) -> dict:
        """Execute comprehensive report generation action."""
        try:
            logger.log_info("Generating comprehensive report...")
            
            # Calculate statistics
            stats_result = self.fs_tools.calculate_detailed_statistics(csv_path)
            if stats_result['status'] != 'success':
                return stats_result
            
            # Check quality
            quality_result = self.fs_tools.check_data_quality(csv_path)
            if quality_result['status'] != 'success':
                return quality_result
            
            # Generate HTML report
            report_result = self.fs_tools.generate_csv_report(
                csv_path,
                stats_result['statistics'],
                quality_result['quality_report']
            )
            
            if report_result['status'] != 'success':
                return report_result
            
            logger.log_info(f"Report generated: {report_result['report_filename']}")
            
            summary = f"""Comprehensive report generated successfully!

**Report Details:**
- File: `{report_result['report_filename']}`
- Location: `{report_result['report_path']}`
- Includes: Statistics, data quality analysis, and visualizations

You can open the HTML report in your web browser to view the full analysis."""
            
            return {
                'status': 'success',
                'action': 'Report Generation',
                'summary': summary,
                'output': summary,
                'report_path': report_result['report_path'],
                'files_created': [report_result['report_path']],
                'message': 'Report generated successfully'
            }
        except Exception as e:
            logger.log_error(0, f"Report generation failed: {str(e)}", e)
            return {
                'status': 'error',
                'message': f'Error generating report: {str(e)}'
            }
    
    def _format_statistics_summary(self, stats: dict) -> str:
        """Format statistics into a readable summary."""
        summary_lines = ["**Statistics Summary:**\n"]
        
        # Overall stats
        overall = stats.get('overall', {})
        summary_lines.append(f"- Total Rows: {overall.get('total_rows', 0)}")
        summary_lines.append(f"- Total Columns: {overall.get('total_columns', 0)}\n")
        
        # Numeric columns
        numeric = stats.get('numeric_columns', {})
        if numeric:
            summary_lines.append("**Numeric Columns:**")
            for col, col_stats in list(numeric.items())[:5]:  # Show first 5
                summary_lines.append(
                    f"- **{col}**: Mean={col_stats['mean']:.2f}, "
                    f"Min={col_stats['min']:.2f}, Max={col_stats['max']:.2f}"
                )
        
        # Categorical columns
        categorical = stats.get('categorical_columns', {})
        if categorical:
            summary_lines.append("\n**Categorical Columns:**")
            for col, col_stats in list(categorical.items())[:5]:  # Show first 5
                summary_lines.append(f"- **{col}**: {col_stats['unique']} unique values")
        
        return '\n'.join(summary_lines)
    
    def _format_quality_summary(self, quality: dict) -> str:
        """Format quality report into a readable summary."""
        summary_lines = ["**Data Quality Report:**\n"]
        
        # Missing values
        missing = quality.get('missing_values', {})
        if missing:
            summary_lines.append("**⚠ Missing Values:**")
            for col, info in list(missing.items())[:5]:
                summary_lines.append(f"- **{col}**: {info['count']} missing ({info['percentage']:.2f}%)")
        else:
            summary_lines.append("✓ No missing values detected")
        
        # Duplicates
        duplicates = quality.get('duplicates', {})
        dup_count = duplicates.get('total_duplicates', 0)
        if dup_count > 0:
            summary_lines.append(f"\n**⚠ Duplicates:** {dup_count} rows ({duplicates['duplicate_percentage']:.2f}%)")
        else:
            summary_lines.append("\n✓ No duplicate rows found")
        
        # Outliers
        outliers = quality.get('outliers', {})
        if outliers:
            summary_lines.append("\n**ℹ Outliers Detected:**")
            for col, info in list(outliers.items())[:5]:
                summary_lines.append(f"- **{col}**: {info['count']} outliers ({info['percentage']:.2f}%)")
        else:
            summary_lines.append("\n✓ No significant outliers detected")
        
        return '\n'.join(summary_lines)


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
