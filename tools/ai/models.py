from django.db import models

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='images/')
    processed_image = models.ImageField(upload_to='images/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"

class TextToSpeech(models.Model):
    text = models.TextField()
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TTS {self.id}"
