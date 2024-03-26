# translator/views.py
from django.shortcuts import render
from django.http import JsonResponse
from playsound import playsound
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os

def translate_view(request):
    if request.method == 'POST':
        # Capture voice input
        query = capture_voice()

        # Translate the input
        translated_text = translate_text(query)

        # Convert translated text to speech
        generate_audio(translated_text)

        return JsonResponse({'translated_text': translated_text})

    return render(request, 'translator/translate.html')

def capture_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing audio.....")
        query = r.recognize_google(audio, language='en-in')
        print(f"The User said {query}\n")
        return query
    except Exception as e:
        print("say that again please.....")
        return None

def translate_text(query):
    translator = Translator()
    to_lang = 'es'  # Example: Translate to Spanish
    translated = translator.translate(query, dest=to_lang)
    return translated.text

def generate_audio(text):
    speak = gTTS(text=text, lang='es', slow=False)
    speak.save("captured_voice.mp3")
    playsound('captured_voice.mp3')
    os.remove('captured_voice.mp3')
