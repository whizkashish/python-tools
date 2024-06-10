from django.urls import path
from . import views

urlpatterns = [
    path('remove-background/', views.remove_background_view, name='remove_background'),
    path('text-to-speech/', views.text_to_speech_view, name='text_to_speech'),
    path('result/<int:pk>/', views.result_view, name='result'),
    path('tts_result/<int:pk>/', views.tts_result_view, name='tts_result'),
]
