from django.db import models
from django.utils import timezone

class GeneratedImage(models.Model):
    prompt = models.TextField()
    negative_prompt = models.TextField(blank=True)
    guidance_scale = models.FloatField(default=7.5)
    num_inference_steps = models.IntegerField(default=30)
    image = models.ImageField(upload_to='generated_images/')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Image generated for: {self.prompt[:50]}..."
