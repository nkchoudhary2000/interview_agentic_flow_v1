"""
Logging utilities for CSV agent actions and other operations.
Provides dual logging to both file and console/terminal.
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import json


class CSVActionLogger:
    """Logger for CSV action executions with dual output (file + console)."""
    
    def __init__(self, base_dir: Path):
        """
        Initialize the CSV action logger.
        
        Args:
            base_dir: Base directory of the project
        """
        self.base_dir = base_dir
        self.logs_dir = base_dir / 'logs'
        self.logs_dir.mkdir(exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger('csv_actions')
        self.logger.setLevel(logging.INFO)
        
        # File handler - daily log file
        log_filename = f"csv_actions_{datetime.now().strftime('%Y-%m-%d')}.log"
        log_filepath = self.logs_dir / log_filename
        
        # Store log file path
        self.current_log_file = str(log_filepath)
        
        # Prevent duplicate logs if logger already configured
        if self.logger.handlers:
            return
        
        file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Console handler - output to terminal
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Format for logs
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_action_start(self, action_id: int, action_name: str, csv_file: str):
        """
        Log the start of a CSV action execution.
        
        Args:
            action_id: ID of the action
            action_name: Name/description of the action
            csv_file: Path to the CSV file being processed
        """
        self.logger.info("="*80)
        self.logger.info(f"Starting CSV Action Execution")
        self.logger.info(f"Action ID: {action_id}")
        self.logger.info(f"Action: {action_name}")
        self.logger.info(f"CSV File: {csv_file}")
        self.logger.info("="*80)
    
    def log_action_result(self, action_id: int, status: str, result: Dict[str, Any]):
        """
        Log the result of a CSV action execution.
        
        Args:
            action_id: ID of the action
            status: Status of execution ('success' or 'error')
            result: Result dictionary from action execution
        """
        self.logger.info(f"Action {action_id} completed with status: {status}")
        
        if status == 'success':
            # Log key result metrics
            if 'output' in result:
                self.logger.info(f"Output summary: {result.get('summary', 'N/A')}")
            
            if 'files_created' in result:
                self.logger.info(f"Files created: {', '.join(result['files_created'])}")
        else:
            self.logger.error(f"Error message: {result.get('message', 'Unknown error')}")
        
        self.logger.info("-"*80)
    
    def log_statistics(self, stats: Dict[str, Any]):
        """
        Log detailed statistics from a statistics action.
        
        Args:
            stats: Statistics dictionary
        """
        self.logger.info("Statistics Calculation Results:")
        self.logger.info(json.dumps(stats, indent=2, default=str))
    
    def log_quality_check(self, quality_report: Dict[str, Any]):
        """
        Log results from a data quality check.
        
        Args:
            quality_report: Quality check results
        """
        self.logger.info("Data Quality Check Results:")
        self.logger.info(json.dumps(quality_report, indent=2, default=str))
    
    def log_error(self, action_id: int, error_message: str, exception: Optional[Exception] = None):
        """
        Log an error during action execution.
        
        Args:
            action_id: ID of the action
            error_message: Error message
            exception: Optional exception object
        """
        self.logger.error(f"Error in Action {action_id}: {error_message}")
        if exception:
            self.logger.error(f"Exception details: {str(exception)}", exc_info=True)
    
    def get_log_file_path(self) -> str:
        """
        Get the path to the current log file.
        
        Returns:
            Absolute path to the current log file
        """
        return self.current_log_file
    
    def log_info(self, message: str):
        """Log an info message."""
        self.logger.info(message)
    
    def log_warning(self, message: str):
        """Log a warning message."""
        self.logger.warning(message)


def get_logger(base_dir: Path) -> CSVActionLogger:
    """
    Get or create a CSV action logger instance.
    
    Args:
        base_dir: Base directory of the project
    
    Returns:
        CSVActionLogger instance
    """
    return CSVActionLogger(base_dir)
