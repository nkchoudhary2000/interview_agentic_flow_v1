"""
Views and API endpoints for the chatbot application.
"""
from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pathlib import Path
import time

from .models import ChatSession, ChatMessage, UploadedFile, AgentExecution
from .serializers import (
    ChatSessionSerializer,
    ChatMessageSerializer,
    ChatMessageCreateSerializer,
    UploadedFileSerializer
)
from agents.router_agent import RouterAgent


def index(request):
    """Render the main chatbot interface."""
    return render(request, 'chatbot/index.html')


@api_view(['POST'])
def create_session(request):
    """Create a new chat session."""
    try:
        session = ChatSession.objects.create(title="New Chat")
        serializer = ChatSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_session(request, session_id):
    """Get a chat session with all messages."""
    try:
        session = ChatSession.objects.get(id=session_id)
        serializer = ChatSessionSerializer(session)
        return Response(serializer.data)
    except ChatSession.DoesNotExist:
        return Response(
            {'error': 'Session not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_messages(request, session_id):
    """Get all messages for a session."""
    try:
        session = ChatSession.objects.get(id=session_id)
        messages = session.messages.all()
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
    except ChatSession.DoesNotExist:
        return Response(
            {'error': 'Session not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def send_message(request):
    """Send a message and get AI response."""
    try:
        serializer = ChatMessageCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        session_id = serializer.validated_data['session_id']
        user_message = serializer.validated_data['message']
        uploaded_file = serializer.validated_data.get('file')
        
        session = ChatSession.objects.get(id=session_id)
        
        # Create user message
        user_msg = ChatMessage.objects.create(
            session=session,
            role='user',
            content=user_message,
            mode='general_chat'
        )
        
        # Handle file upload if present
        uploaded_file_info = None
        if uploaded_file:
            uploaded_file_info = _handle_file_upload(session, user_msg, uploaded_file)
        
        # Process message with router agent
        start_time = time.time()
        
        try:
            router = RouterAgent(
                api_key=settings.GROQ_API_KEY,
                base_dir=Path(settings.BASE_DIR)
            )
            
            result = router.process_message(
                message=user_message,
                uploaded_file=uploaded_file_info
            )
            
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            # Create assistant response message
            assistant_msg = _create_assistant_message(session, result)
            
            # Log agent execution
            AgentExecution.objects.create(
                session=session,
                message=assistant_msg,
                agent_type='router',
                input_data={'message': user_message, 'file': uploaded_file_info},
                output_data=result,
                execution_time_ms=execution_time_ms,
                success=result.get('status') == 'success'
            )
            
            # Update session timestamp
            session.updated_at = timezone.now()
            session.save()
            
            # Return both messages
            return Response({
                'user_message': ChatMessageSerializer(user_msg).data,
                'assistant_message': ChatMessageSerializer(assistant_msg).data,
                'execution_time_ms': execution_time_ms
            })
            
        except Exception as e:
            # Create error message
            error_msg = ChatMessage.objects.create(
                session=session,
                role='assistant',
                content=f"I encountered an error: {str(e)}",
                mode='error',
                metadata={'error': str(e)}
            )
            
            return Response({
                'user_message': ChatMessageSerializer(user_msg).data,
                'assistant_message': ChatMessageSerializer(error_msg).data,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def upload_file(request):
    """Handle file upload."""
    try:
        session_id = request.data.get('session_id')
        uploaded_file = request.FILES.get('file')
        
        if not session_id or not uploaded_file:
            return Response(
                {'error': 'session_id and file are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        session = ChatSession.objects.get(id=session_id)
        
        # Determine file type
        file_ext = uploaded_file.name.lower().split('.')[-1]
        file_type = 'pdf' if file_ext == 'pdf' else 'csv' if file_ext == 'csv' else 'other'
        
        # Create UploadedFile record
        file_record = UploadedFile.objects.create(
            session=session,
            file=uploaded_file,
            file_type=file_type,
            original_filename=uploaded_file.name,
            status='completed'
        )
        
        serializer = UploadedFileSerializer(file_record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except ChatSession.DoesNotExist:
        return Response(
            {'error': 'Session not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def execute_csv_action(request):
    """Execute a CSV action selected by the user."""
    try:
        session_id = request.data.get('session_id')
        action_id = request.data.get('action_id')
        csv_path = request.data.get('csv_path')
        analysis = request.data.get('analysis', {})
        
        print(f"[DEBUG] execute_csv_action called")
        print(f"[DEBUG] session_id: {session_id}")
        print(f"[DEBUG] action_id: {action_id}")
        print(f"[DEBUG] csv_path: {csv_path}")
        print(f"[DEBUG] analysis keys: {analysis.keys() if analysis else 'None'}")
        
        if not all([session_id, action_id, csv_path]):
            error_msg = f'Missing required fields: session_id={session_id}, action_id={action_id}, csv_path={csv_path}'
            print(f"[ERROR] {error_msg}")
            return Response(
                {'error': 'session_id, action_id, and csv_path are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        session = ChatSession.objects.get(id=session_id)
        print(f"[DEBUG] Session found: {session.id}")
        
        # Execute action using router agent
        router = RouterAgent(
            api_key=settings.GROQ_API_KEY,
            base_dir=Path(settings.BASE_DIR)
        )
        
        print(f"[DEBUG] Calling router.execute_csv_action...")
        result = router.execute_csv_action(csv_path, action_id, analysis)
        print(f"[DEBUG] Result status: {result.get('status')}")
        print(f"[DEBUG] Result message: {result.get('message', 'No message')}")
        
        # Create assistant message with result
        assistant_msg = _create_assistant_message(session, result)
        print(f"[DEBUG] Assistant message created: {assistant_msg.id}")
        
        return Response({
            'assistant_message': ChatMessageSerializer(assistant_msg).data,
            'result': result
        })
        
    except ChatSession.DoesNotExist:
        print(f"[ERROR] Session not found: {session_id}")
        return Response(
            {'error': 'Session not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"[ERROR] Exception in execute_csv_action:")
        print(error_trace)
        return Response(
            {'error': str(e), 'traceback': error_trace},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def _handle_file_upload(session, message, uploaded_file):
    """Handle file upload and return file info."""
    file_ext = uploaded_file.name.lower().split('.')[-1]
    file_type = 'pdf' if file_ext == 'pdf' else 'csv' if file_ext == 'csv' else 'other'
    
    # Create UploadedFile record
    file_record = UploadedFile.objects.create(
        session=session,
        message=message,
        file=uploaded_file,
        file_type=file_type,
        original_filename=uploaded_file.name,
        status='processing'
    )
    
    # Return file info for agent
    return {
        'path': file_record.file.path,
        'type': file_type,
        'name': uploaded_file.name
    }


def _create_assistant_message(session, result):
    """Create assistant message from agent result."""
    mode = result.get('mode', 'general_chat')
    
    # Format content based on mode
    if mode == 'code_generation':
        content = _format_code_generation_response(result)
    elif mode == 'pdf_extraction':
        content = _format_pdf_response(result)
    elif mode == 'csv_analysis':
        content = _format_csv_response(result)
    elif mode == 'csv_action':
        content = _format_csv_action_response(result)
    else:
        content = result.get('message', 'Response generated')
    
    # Create message
    return ChatMessage.objects.create(
        session=session,
        role='assistant',
        content=content,
        mode=mode,
        metadata=result
    )


def _format_code_generation_response(result):
    """Format code generation response."""
    if result.get('status') != 'success':
        return f"Error: {result.get('message', 'Unknown error')}"
    
    return f"""I've generated the code and saved it to `{result.get('filename', 'file')}`.

**Generated Code:**
```{result.get('language', 'python')}
{result.get('code', '')}
```

**Code Review:**
{result.get('review', 'No review available')}

**File Location:** `{result.get('filepath', 'N/A')}`
"""


def _format_pdf_response(result):
    """Format PDF extraction response."""
    if result.get('status') != 'success':
        return f"Error: {result.get('message', 'Unknown error')}"
    
    return f"""PDF extracted successfully!

**Summary:** {result.get('summary', 'Extraction complete')}

**Statistics:**
- Pages: {result.get('page_count', 0)}
- Words: {result.get('word_count', 0)}
- Saved to: `{result.get('filepath', 'N/A')}`
"""


def _format_csv_response(result):
    """Format CSV analysis response."""
    if result.get('status') != 'success':
        return f"Error: {result.get('message', 'Unknown error')}"
    
    content = f"""CSV Analysis Complete!

**File:** {result.get('filename', 'Unknown')}
**Content Summary:** {result.get('content_summary', 'N/A')}

**Statistics:**
- Rows: {result.get('num_rows', 0)}
- Columns: {result.get('num_cols', 0)}

**Suggestions for working with this data:**
"""
    
    suggestions = result.get('suggestions', [])
    for suggestion in suggestions:
        content += f"\n{suggestion.get('id')}. **{suggestion.get('title')}**: {suggestion.get('description')}"
    
    return content


def _format_csv_action_response(result):
    """Format CSV action execution response."""
    if result.get('status') != 'success':
        return f"Error: {result.get('message', 'Unknown error')}"
    
    action_name = result.get('action', 'CSV Action')
    
    content = f"""✅ **{action_name} Completed!**

{result.get('output', result.get('summary', 'Action executed successfully'))}
"""
    
    # Add files created if any
    if result.get('files_created'):
        content += "\n\n**Files Created:**"
        for file_path in result['files_created']:
            from pathlib import Path
            filename = Path(file_path).name
            content += f"\n- `{filename}` - {file_path}"
    
    # Add log file information
    if result.get('log_file'):
        from pathlib import Path
        log_filename = Path(result['log_file']).name
        content += f"\n\n**📋 Execution Log:** `{log_filename}`\n*Check the terminal output or log file for detailed execution information.*"
    
    return content
