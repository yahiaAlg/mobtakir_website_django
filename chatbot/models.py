import os
from django.db import models

# Create your models here.
# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ChatSession(models.Model):
    LANGUAGE_CHOICES = [
        ("english", "english"),
        ("arabic", "arabic"),
        ("french", "french"),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chat_sessions"
    )
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    model_name = models.CharField(
        max_length=50, default="phi3"
    )  # or whatever default model you're using
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default="english")
    temperature = models.DecimalField(max_digits=2, decimal_places=1)
    max_tokens = models.IntegerField(
        default=1050
    )
    context_memory = models.IntegerField(
        default=5
    )
    auto_correct = models.BooleanField(default=False)
    temperature = models.DecimalField(max_digits=2, decimal_places=1, default=0.7)
    api_key = models.CharField(max_length=50, blank=True, null=True, default=os.getenv("GOOGLE_API_KEY"))
    
    endpoint_url = models.URLField(max_length=200, blank=True, null=True)
    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.user.username}'s chat - {self.title or self.created_at}"


class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ("user", "User"),
        ("assistant", "Assistant"),
        ("system", "System"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("error", "Error"),
    ]

    session = models.ForeignKey(
        ChatSession, on_delete=models.CASCADE, related_name="messages"
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="completed"
    )
    error_message = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.role} - {self.timestamp}"

    @property
    def time_formatted(self):
        return self.timestamp.strftime("%I:%M %p")
