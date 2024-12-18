import os
import base64
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.base import ContentFile
from django.conf import settings
from .forms import AudioGenerationForm
from .models import GeneratedAudio

def generate_audio(request):
    if request.method == 'POST':
        form = AudioGenerationForm(request.POST)
        if form.is_valid():
            try:
                # API configuration
                api_url = f"{form.cleaned_data['api_url'] or settings.AUDIO_API_URL }/generate-audio"
                
                # Prepare the request
                data = {
                    "prompt": form.cleaned_data['prompt'],
                    "negative_prompt": form.cleaned_data['negative_prompt'],
                    "audio_length": form.cleaned_data['audio_length'],
                    "guidance_scale": form.cleaned_data['guidance_scale'],
                    "num_inference_steps": form.cleaned_data['num_inference_steps'],
                }

                # Make API request
                response = requests.post(api_url, json=data, timeout=300)
                response.raise_for_status()
                result = response.json()

                if result.get("status") == "success":
                    # Create model instance but don't save yet
                    audio_instance = form.save(commit=False)
                    
                    # Convert base64 to audio file
                    audio_data = base64.b64decode(result["audio_base64"])
                    audio_file = ContentFile(audio_data)
                    
                    # Generate unique filename
                    filename = f"generated_{audio_instance.created_at.strftime('%Y%m%d_%H%M%S')}.wav"
                    
                    # Save audio file
                    audio_instance.audio_file.save(filename, audio_file, save=False)
                    audio_instance.save()
                    
                    messages.success(request, 'Audio generated successfully!')
                    return redirect('audio_gen:gallery')
                else:
                    messages.error(request, f"API Error: {result.get('detail', 'Unknown error')}")

            except requests.exceptions.RequestException as e:
                messages.error(request, f"Request Error: {str(e)}")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
    else:
        form = AudioGenerationForm(initial={
            'audio_length': 5.0,
            'num_inference_steps': 10,
            'guidance_scale': 2.5,
        })
    
    return render(request, 'audio_generator/generate.html', {'form': form})

def gallery(request):
    audios = GeneratedAudio.objects.all()
    return render(request, 'audio_generator/gallery.html', {'audios': audios})
