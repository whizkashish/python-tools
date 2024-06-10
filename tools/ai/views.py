from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from .forms import ImageUploadForm, TextToSpeechForm
from .models import ImageUpload, TextToSpeech
from pydub import AudioSegment
from rembg import remove
from PIL import Image
import pyttsx3
import os

def remove_background_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_upload = form.save()
            input_path = image_upload.image.path
            output_path = os.path.splitext(input_path)[0] + '_bg_removed.png'

            with Image.open(input_path) as img:
                output = remove(img)
                output.save(output_path)

            image_upload.processed_image = output_path
            image_upload.save()

            return redirect('result', pk=image_upload.pk)
    else:
        form = ImageUploadForm()
    return render(request, 'ai/upload_image.html', {'form': form})

def text_to_speech_view(request):
    if request.method == 'POST':
        form = TextToSpeechForm(request.POST)
        if form.is_valid():
            tts_entry = form.save()
            engine = pyttsx3.init()
            media_path = f'{settings.MEDIA_ROOT}/audio/'
            if not os.path.exists(media_path):
                os.makedirs(media_path)
            temp_wav_file = f'{media_path}{tts_entry.id}.wav'
            final_mp3_file = f'{media_path}{tts_entry.id}.mp3'

            # Save to WAV format first
            engine.save_to_file(tts_entry.text, temp_wav_file)
            engine.runAndWait()

            # Convert WAV to MP3
            sound = AudioSegment.from_wav(temp_wav_file)
            sound.export(final_mp3_file, format="mp3")

            # Clean up temporary WAV file
            # os.remove(temp_wav_file)

            tts_entry.audio_file = f'audio/{tts_entry.id}.mp3'
            tts_entry.save()

            return redirect('tts_result', pk=tts_entry.pk)
    else:
        form = TextToSpeechForm()
    return render(request, 'ai/text_to_speech.html', {'form': form})

def result_view(request, pk):
    image_upload = ImageUpload.objects.get(pk=pk)
    return render(request, 'ai/result.html', {'image_upload': image_upload})

def tts_result_view(request, pk):
    tts_entry = TextToSpeech.objects.get(pk=pk)
    return render(request, 'ai/tts_result.html', {'tts_entry': tts_entry})
