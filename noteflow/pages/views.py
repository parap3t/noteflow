import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .forms import LoginForm, RegisterForm
from .models import Note
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'pages/index.html')


def about(request):
    return render(request, 'pages/about.html')


def login_view(request):

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:

                login(request, user)

                return redirect('notes')

            else:
                form.add_error('username', 'Неверный логин или пароль')

    else:
        form = LoginForm()  # Пустая форма при GET-запросе

    return render(request, 'pages/login.html', {'form': form})


def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)

            return redirect('notes')

    else:
        form = RegisterForm()

    return render(request, 'pages/registration.html', {'form': form})


# Главная страница с заметками
@login_required
def notes(request):
    user_notes = Note.objects.filter(user=request.user)
    return render(request, 'pages/notes.html', {'notes': user_notes})


# Создание новой заметки
@login_required
@require_POST  # Проверяем, что запрос является POST
@csrf_protect  # Защищаем от CSRF атак
def create_note(request):

    try:

        data = json.loads(request.body)
        text = data.get('text', '').strip()

        if not text:
            return JsonResponse({'status': 'error', 'message': 'Текст заметки не может быть пустым'})

        note = Note.objects.create(user=request.user, text=text)

        return JsonResponse({
            'status': 'success',
            'message': 'Заметка создана',
            'note': {'id': note.id, 'text': note.text}
        })

    except (json.JSONDecodeError, Exception) as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


# Редактирование заметки
@login_required
@require_POST  # Проверяем, что запрос является POST
@csrf_protect  # Защищаем от CSRF атак
def edit_note(request, note_id):

    try:

        note = get_object_or_404(Note, id=note_id, user=request.user)
        data = json.loads(request.body)
        new_text = data.get('text', '').strip()

        if not new_text:
            return JsonResponse({'status': 'error', 'message': 'Текст заметки не может быть пустым'})

        note.text = new_text
        note.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Заметка обновлена',
            'note': {'id': note.id, 'text': note.text}
        })

    except (json.JSONDecodeError, Exception) as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required
@require_POST  # Проверяем, что запрос является POST
@csrf_protect  # Защищаем от CSRF атак
def delete_note(request, note_id):
    try:
        # Получаем заметку по её id
        note = get_object_or_404(Note, id=note_id, user=request.user)

        # Удаляем заметку
        note.delete()

        # Возвращаем успешный ответ
        return JsonResponse({'status': 'success', 'message': 'Заметка удалена'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})