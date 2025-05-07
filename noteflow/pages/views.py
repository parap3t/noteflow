from django.shortcuts import render
from django.contrib.auth.decorators import login_required  # Импортируем декоратор

from .models import Note


def home(request):
    return render(request, 'pages/index.html')

def about(request):
    return render(request, 'pages/about.html')


@login_required
def notes(request):

    # Получаем все заметки текущего пользователя
    user_notes = Note.objects.filter(user=request.user)

    return render(request, 'pages/notes.html', {'notes': user_notes})