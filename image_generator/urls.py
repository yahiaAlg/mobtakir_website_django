from django.urls import path
from . import views
app_name = "image_gen"
urlpatterns = [
    path('', views.generate_image, name='generate'),
    path('gallery/', views.gallery, name='gallery'),
]
