from django.urls import path
from . import views

app_name = "chat_upload"

urlpatterns = [
    path("", views.index, name="index"),
]
