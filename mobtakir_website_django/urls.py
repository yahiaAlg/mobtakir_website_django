from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("accounts/", include("accounts.urls")),
        path("social/", include("social_django.urls", namespace="social")),
        path("", include("pages.urls", "pages")),
        path("blog/", include("blog.urls", "blog")),
        path("chatbot/", include("chatbot.urls", "chatbot")),
        path("chat/", include("chat.urls", "chat_upload")),
        path("image-gen/", include("image_generator.urls", "image_gen")),
        path("audio-gen/", include("audio_generator.urls", "audio_gen")),

    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
