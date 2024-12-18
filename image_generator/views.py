import os
import base64
import requests
from io import BytesIO
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.base import ContentFile
from django.conf import settings
from .forms import ImageGenerationForm
from .models import GeneratedImage

def generate_image(request):
    if request.method == 'POST':
        form = ImageGenerationForm(request.POST)
        if form.is_valid():
            try:
                # API configuration by either bringing it from settings or getting it from the API text Field 
                api_url = form.cleaned_data['api_url'] or settings.STABLE_DIFFUSION_API_URL
                print(
                    f"API URL: {api_url}"
                )
                api_key = settings.STABLE_DIFFUSION_API_KEY

                # Prepare the request
                headers = {
                    "X-API-Key": api_key,
                    "Content-Type": "application/json"
                }
                
                data = {
                    "prompt": form.cleaned_data['prompt'],
                    "negative_prompt": form.cleaned_data['negative_prompt'],
                    "guidance_scale": form.cleaned_data['guidance_scale'],
                    "num_inference_steps": form.cleaned_data['num_inference_steps'],
                }

                # Make API request
                response = requests.post(
                    f"{api_url}/generate/",
                    headers=headers,
                    json=data,
                    timeout=300
                )
                response.raise_for_status()
                result = response.json()

                if result["status"] == "success":
                    # Create model instance but don't save yet
                    image_instance = form.save(commit=False)
                    
                    # Convert base64 to image file
                    image_data = base64.b64decode(result["image"])
                    image_file = ContentFile(image_data)
                    
                    # Generate unique filename
                    filename = f"generated_{image_instance.created_at.strftime('%Y%m%d_%H%M%S')}.jpg"
                    
                    # Save image file
                    image_instance.image.save(filename, image_file, save=False)
                    image_instance.save()
                    
                    messages.success(request, 'Image generated successfully!')
                    return redirect('image_gen:gallery')
                else:
                    messages.error(request, f"API Error: {result.get('message', 'Unknown error')}")

            except requests.exceptions.RequestException as e:
                messages.error(request, f"Request Error: {str(e)}")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
    else:
        form = ImageGenerationForm()
    
    return render(request, 'image_generator/generate.html', {'form': form})

def gallery(request):
    images = GeneratedImage.objects.all()
    return render(request, 'image_generator/gallery.html', {'images': images})
