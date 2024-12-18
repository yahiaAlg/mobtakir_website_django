from django import forms
from .models import GeneratedImage

class ImageGenerationForm(forms.ModelForm):
    class Meta:
        model = GeneratedImage
        fields = ['prompt', 'negative_prompt', 'guidance_scale', 'num_inference_steps']
        widgets = {
            'prompt': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'negative_prompt': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'guidance_scale': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '1.0', 'max': '20.0'}),
            'num_inference_steps': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '100'}),
        }
