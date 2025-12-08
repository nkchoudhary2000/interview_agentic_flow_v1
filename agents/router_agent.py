"""
Router Agent - Main orchestrator using Groq API.
"""
from groq import Groq
from .code_gen_agent import CodeGenerationAgent
from .pdf_agent import PDFExtractionAgent
from .csv_agent import CSVAnalysisAgent
from .tools import FileSystemTools
from pathlib import Path
import json


class RouterAgent:
    """
    Main orchestrator agent that analyzes user intent and routes to specialized agents.
    """
    
    def __init__(self, api_key: str, base_dir: Path):
        self.client = Groq(api_key=api_key)
        self.api_key = api_key
        self.base_dir = base_dir
        self.model_id = "llama-3.3-70b-versatile"
        
        # Initialize tools and specialized agents
        self.fs_tools = FileSystemTools(base_dir)
        self.code_gen_agent = CodeGenerationAgent(api_key, self.fs_tools)
        self.pdf_agent = PDFExtractionAgent(api_key, self.fs_tools)
        self.csv_agent = CSVAnalysisAgent(api_key, self.fs_tools)
    
    def process_message(self, message: str, uploaded_file: dict = None) -> dict:
        """
        Process user message and route to appropriate agent.
        
        Args:
            message: User's message
            uploaded_file: Optional dict with 'path' and 'type' keys
        
        Returns:
            dict with response and metadata
        """
        try:
            # Determine intent and route
            if uploaded_file:
                return self._handle_file_upload(message, uploaded_file)
            else:
                return self._handle_text_message(message)
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error processing request: {str(e)}',
                'mode': 'error'
            }
    
    def _handle_file_upload(self, message: str, uploaded_file: dict) -> dict:
        """Handle file upload requests."""
        file_path = uploaded_file['path']
        file_type = uploaded_file['type']
        
        if file_type == 'pdf' or file_path.lower().endswith('.pdf'):
            # Route to PDF agent
            result = self.pdf_agent.process_pdf(file_path)
            result['mode'] = 'pdf_extraction'
            result['user_message'] = message
            return result
            
        elif file_type == 'csv' or file_path.lower().endswith('.csv'):
            # Route to CSV agent
            result = self.csv_agent.analyze_csv(file_path)
            result['mode'] = 'csv_analysis'
            result['user_message'] = message
            result['file_path'] = file_path  # Store for later action execution
            return result
            
        else:
            return {
                'status': 'error',
                'message': f'Unsupported file type: {file_type}. Please upload PDF or CSV files.',
                'mode': 'error'
            }
    
    def _handle_text_message(self, message: str) -> dict:
        """Handle text-only messages."""
        # Detect intent using Groq
        intent = self._detect_intent(message)
        
        if intent['type'] == 'code_generation':
            # Route to code generation agent
            result = self.code_gen_agent.generate_code(
                user_prompt=message,
                language=intent.get('language', 'python')
            )
            result['mode'] = 'code_generation'
            result['user_message'] = message
            return result
            
        elif intent['type'] == 'general_chat':
            # Handle general conversation
            result = self._handle_general_chat(message)
            result['mode'] = 'general_chat'
            return result
            
        else:
            # Default to general chat
            result = self._handle_general_chat(message)
            result['mode'] = 'general_chat'
            return result
    
    def _detect_intent(self, message: str) -> dict:
        """
        Detect user intent from message using Groq.
        
        Returns:
            dict with 'type' and optional 'language'
        """
        try:
            prompt = f"""Analyze this user message and determine the intent.

USER MESSAGE: "{message}"

Determine if the user is:
1. Requesting code generation (keywords: write, create, generate, code, function, class, script, program, etc.)
2. General chat/question

Also detect programming language if code generation is requested (python, javascript, java, etc.)

Respond in JSON format:
{{
  "type": "code_generation" or "general_chat",
  "language": "python" (only if code_generation, otherwise omit),
  "confidence": 0.0 to 1.0
}}

Return ONLY valid JSON, no additional text.
"""
            
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=150
            )
            
            # Parse JSON response
            response_text = response.choices[0].message.content.strip()
            
            # Extract JSON from response
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            intent = json.loads(response_text)
            
            # If confidence is low, default to general chat
            if intent.get('confidence', 0) < 0.6:
                intent['type'] = 'general_chat'
            
            return intent
            
        except Exception:
            # Default to general chat on error
            return {'type': 'general_chat'}
    
    def _handle_general_chat(self, message: str) -> dict:
        """Handle general chat messages using Groq."""
        try:
            # Create context-aware response
            system_message = """You are a helpful AI assistant in a chatbot that can:
1. Generate code when requested (just ask me to write any code!)
2. Extract text from PDF files when uploaded
3. Analyze CSV files and provide intelligent suggestions when uploaded

For general questions, provide helpful and concise responses."""
            
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return {
                'status': 'success',
                'message': response.choices[0].message.content.strip(),
                'user_message': message
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error processing message: {str(e)}'
            }
    
    def execute_csv_action(self, csv_path: str, action_id: int, analysis: dict) -> dict:
        """
        Execute a CSV action selected by the user.
        
        Args:
            csv_path: Path to CSV file
            action_id: Selected action ID
            analysis: Previous analysis result
        
        Returns:
            dict with action result
        """
        try:
            result = self.csv_agent.execute_action(csv_path, action_id, analysis)
            result['mode'] = 'csv_action'
            return result
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error executing action: {str(e)}',
                'mode': 'error'
            }


# Standalone function for easy integration with Django
def process_chat_message(api_key: str, message: str, base_dir: Path, uploaded_file: dict = None) -> dict:
    """
    Convenience function to process chat messages.
    
    Args:
        api_key: Groq API key
        message: User message
        base_dir: Base directory for file operations
        uploaded_file: Optional uploaded file info
    
    Returns:
        dict with response and metadata
    """
    router = RouterAgent(api_key, base_dir)
    return router.process_message(message, uploaded_file)
