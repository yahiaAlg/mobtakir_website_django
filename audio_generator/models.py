from django.db import models
from django.utils import timezone

class GeneratedAudio(models.Model):
    prompt = models.TextField()
    negative_prompt = models.TextField(blank=True, null=True)
    audio_length = models.FloatField(default=5.0)
    guidance_scale = models.FloatField(default=2.5)
    num_inference_steps = models.IntegerField(default=10)
    audio_file = models.FileField(upload_to='generated_audio/')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Audio generated for: {self.prompt[:50]}..."
