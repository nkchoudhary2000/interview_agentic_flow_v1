"""
Django admin configuration for chatbot models.
"""
from django.contrib import admin
from .models import ChatSession, ChatMessage, UploadedFile, AgentExecution


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'role', 'mode', 'created_at')
    list_filter = ('role', 'mode', 'created_at')
    search_fields = ('content', 'session__id')
    readonly_fields = ('id', 'created_at')


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_filename', 'file_type', 'status', 'uploaded_at')
    list_filter = ('file_type', 'status', 'uploaded_at')
    search_fields = ('original_filename', 'session__id')
    readonly_fields = ('id', 'uploaded_at', 'processed_at')


@admin.register(AgentExecution)
class AgentExecutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'agent_type', 'success', 'execution_time_ms', 'created_at')
    list_filter = ('agent_type', 'success', 'created_at')
    search_fields = ('session__id', 'error_message')
    readonly_fields = ('id', 'created_at')
