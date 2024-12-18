from django.shortcuts import render
from django.conf import settings
def index(request):
        
    return render(request, 'chat/index.html', {'chat_api_url': settings.CHAT_API_URL})
