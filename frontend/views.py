from django.shortcuts import render

def home(request):
    supported_languages = {
        "eng": "English",
        "rus": "Русский",
        "spa": "Español",
        # Другие языки добавляем здесь
    }
    return render(request, 'frontend/home.html', {'supported_languages': supported_languages})
