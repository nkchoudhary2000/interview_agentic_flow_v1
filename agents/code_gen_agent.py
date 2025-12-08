"""
Code Generation Agent using Groq API.
"""
from groq import Groq
from .tools import FileSystemTools


class CodeGenerationAgent:
    """Agent that generates code, reviews it, and saves to filesystem using Groq."""
    
    def __init__(self, api_key: str, fs_tools: FileSystemTools):
        self.client = Groq(api_key=api_key)
        self.fs_tools = fs_tools
        self.model_id = "llama-3.3-70b-versatile"  # Groq's best model
    
    def generate_code(self, user_prompt: str, language: str = 'python') -> dict:
        """
        Generate code based on user prompt, review it, and save to file.
        
        Args:
            user_prompt: User's code generation request
            language: Programming language to generate code in
        
        Returns:
            dict with generated code, review, and file path
        """
        try:
            # Step 1: Generate code with structured template
            generation_prompt = self._create_generation_template(user_prompt, language)
            
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": generation_prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            
            generated_code = response.choices[0].message.content.strip()
            
            # Extract code from markdown code blocks if present
            if '```' in generated_code:
                lines = generated_code.split('\n')
                code_lines = []
                in_code_block = False
                for line in lines:
                    if line.startswith('```'):
                        in_code_block = not in_code_block
                        continue
                    if in_code_block:
                        code_lines.append(line)
                generated_code = '\n'.join(code_lines)
            
            # Step 2: Review the generated code
            review_result = self._review_code(generated_code, language, user_prompt)
            
            # Step 3: Save to filesystem
            filename = self._generate_filename(user_prompt, language)
            save_result = self.fs_tools.save_code_to_file(
                code=generated_code,
                filename=filename,
                language=language
            )
            
            return {
                'status': 'success',
                'code': generated_code,
                'review': review_result,
                'filepath': save_result.get('filepath'),
                'filename': filename,
                'language': language,
                'message': 'Code generated, reviewed, and saved successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'code': '',
                'review': '',
                'filepath': None,
                'message': f'Error generating code: {str(e)}'
            }
    
    def _create_generation_template(self, user_prompt: str, language: str) -> str:
        """Create a structured template for code generation."""
        template = f"""You are an expert {language} programmer. Generate clean, efficient, and well-documented code.

USER REQUEST: {user_prompt}

INSTRUCTIONS:
1. Write production-quality {language} code that fulfills the user's request
2. Include clear comments explaining the logic
3. Follow {language} best practices and style guidelines
4. Make the code modular and reusable
5. Include error handling where appropriate
6. Add docstrings/documentation for functions and classes

Generate ONLY the code, without additional explanations or markdown formatting.
"""
        return template
    
    def _review_code(self, code: str, language: str, original_prompt: str) -> str:
        """Review the generated code for quality and correctness."""
        try:
            review_prompt = f"""You are a senior code reviewer. Review this {language} code and provide constructive feedback.

ORIGINAL REQUEST: {original_prompt}

CODE TO REVIEW:
```{language}
{code}
```

Provide a concise review covering:
1. **Correctness**: Does it fulfill the requirements?
2. **Quality**: Code organization, readability, best practices
3. **Security**: Any potential security issues?
4. **Performance**: Any performance concerns?
5. **Suggestions**: 1-2 key improvements (if any)

Keep the review brief and actionable (200 words max).
"""
            
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": review_prompt}],
                temperature=0.5,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Review unavailable: {str(e)}"
    
    def _generate_filename(self, prompt: str, language: str) -> str:
        """Generate a meaningful filename from the prompt."""
        # Extract key words from prompt
        words = prompt.lower().split()
        
        # Filter common words
        stop_words = {'a', 'an', 'the', 'to', 'for', 'of', 'in', 'on', 'with', 'write', 'create', 'make', 'code'}
        meaningful_words = [w for w in words if w not in stop_words and w.isalnum()]
        
        # Take first 3-4 meaningful words
        filename_parts = meaningful_words[:4]
        
        if not filename_parts:
            filename_parts = ['generated_code']
        
        filename = '_'.join(filename_parts)
        
        # Truncate if too long
        if len(filename) > 50:
            filename = filename[:50]
        
        return filename


# Standalone function for easy integration
def generate_and_save_code(api_key: str, user_prompt: str, base_dir, language: str = 'python') -> dict:
    """
    Convenience function to generate code.
    
    Args:
        api_key: Groq API key
        user_prompt: User's code request
        base_dir: Base directory for file operations
        language: Programming language
    
    Returns:
        dict with code, review, and filepath
    """
    fs_tools = FileSystemTools(base_dir)
    agent = CodeGenerationAgent(api_key, fs_tools)
    return agent.generate_code(user_prompt, language)
