"""
Serializers for chatbot API.
"""
from rest_framework import serializers
from .models import ChatSession, ChatMessage, UploadedFile


class ChatMessageSerializer(serializers.ModelSerializer):
    """Serializer for chat messages."""
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'role', 'content', 'mode', 'metadata', 'created_at']
        read_only_fields = ['id', 'created_at']


class ChatSessionSerializer(serializers.ModelSerializer):
    """Serializer for chat sessions."""
    
    messages = ChatMessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatSession
        fields = ['id', 'title', 'created_at', 'updated_at', 'messages', 'message_count']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_message_count(self, obj):
        return obj.messages.count()


class UploadedFileSerializer(serializers.ModelSerializer):
    """Serializer for uploaded files."""
    
    class Meta:
        model = UploadedFile
        fields = ['id', 'file', 'file_type', 'original_filename', 'status', 'result', 'uploaded_at', 'processed_at']
        read_only_fields = ['id', 'status', 'result', 'uploaded_at', 'processed_at']


class ChatMessageCreateSerializer(serializers.Serializer):
    """Serializer for creating chat messages."""
    
    session_id = serializers.UUIDField()
    message = serializers.CharField()
    file = serializers.FileField(required=False, allow_null=True)
    
    def validate_session_id(self, value):
        """Validate that session exists."""
        if not ChatSession.objects.filter(id=value).exists():
            raise serializers.ValidationError("Session not found")
        return value
