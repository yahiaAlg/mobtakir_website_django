from django import forms
from .models import GeneratedAudio

class AudioGenerationForm(forms.ModelForm):
    class Meta:
        model = GeneratedAudio
        fields = ['prompt', 'negative_prompt', 'audio_length', 'guidance_scale', 'num_inference_steps']
        widgets = {
            'prompt': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'form-control',
                'placeholder': 'Enter your audio description (e.g., "Techno music with a strong, upbeat tempo")'
            }),
            'negative_prompt': forms.Textarea(attrs={
                'rows': 2, 
                'class': 'form-control',
                'placeholder': 'Enter what you don\'t want in the audio (optional)'
            }),
            'audio_length': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.5',
                'min': '1.0',
                'max': '30.0'
            }),
            'guidance_scale': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '1.0',
                'max': '20.0'
            }),
            'num_inference_steps': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '50'
            }),
        }
