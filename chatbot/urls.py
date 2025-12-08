"""
URL configuration for chatbot app.
"""
from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    # Main chatbot interface
    path('', views.index, name='index'),
    
    # API endpoints
    path('api/chat/sessions/', views.create_session, name='create_session'),
    path('api/chat/sessions/<uuid:session_id>/', views.get_session, name='get_session'),
    path('api/chat/sessions/<uuid:session_id>/messages/', views.get_messages, name='get_messages'),
    path('api/chat/message/', views.send_message, name='send_message'),
    path('api/chat/upload/', views.upload_file, name='upload_file'),
    path('api/chat/action/', views.execute_csv_action, name='execute_csv_action'),
]
