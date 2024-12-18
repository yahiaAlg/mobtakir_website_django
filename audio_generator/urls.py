from django.urls import path
from . import views
app_name = 'audio_gen'
urlpatterns = [
    path('', views.generate_audio, name='generate'),
    path('gallery/', views.gallery, name='gallery'),
]
