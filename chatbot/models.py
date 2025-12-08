"""
Django models for the chatbot application.
"""
from django.db import models
from django.utils import timezone
import uuid


class ChatSession(models.Model):
    """Represents a chat session."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255, default="New Chat")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Session {self.id} - {self.title}"


class ChatMessage(models.Model):
    """Represents a single message in a chat session."""
    
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]
    
    MODE_CHOICES = [
        ('general_chat', 'General Chat'),
        ('code_generation', 'Code Generation'),
        ('pdf_extraction', 'PDF Extraction'),
        ('csv_analysis', 'CSV Analysis'),
        ('csv_action', 'CSV Action'),
        ('error', 'Error'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='general_chat')
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."


class UploadedFile(models.Model):
    """Tracks uploaded files and their processing status."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    FILE_TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('csv', 'CSV'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='files')
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name='files', null=True, blank=True)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    original_filename = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    result = models.JSONField(default=dict, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.original_filename} - {self.status}"


class AgentExecution(models.Model):
    """Logs agent executions for debugging and analytics."""
    
    AGENT_CHOICES = [
        ('router', 'Router Agent'),
        ('code_gen', 'Code Generation Agent'),
        ('pdf', 'PDF Extraction Agent'),
        ('csv', 'CSV Analysis Agent'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='executions')
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name='executions')
    agent_type = models.CharField(max_length=20, choices=AGENT_CHOICES)
    input_data = models.JSONField(default=dict)
    output_data = models.JSONField(default=dict)
    execution_time_ms = models.IntegerField(null=True, blank=True)
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.agent_type} - {self.created_at}"
