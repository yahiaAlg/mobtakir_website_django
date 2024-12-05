from django.urls import path
from . import views

app_name = "chatbot"
urlpatterns = [
    path("chat/", views.chat_view, name="chat"),
    path(
        "chat/history/<int:session_id>/", views.chat_history_view, name="chat_history"
    ),
    path("chat/sessions/", views.chat_sessions_view, name="chat_sessions"),
    path("chat/chat_settings/", views.chat_settings, name="chat_settings"),
    path("chat/load_settings/", views.load_chat_settings, name="load_chat_settings"),
]
