from django import forms
from .models import ImageUpload, TextToSpeech

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']

class TextToSpeechForm(forms.ModelForm):
    class Meta:
        model = TextToSpeech
        fields = ['text']
