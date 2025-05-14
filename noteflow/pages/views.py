from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required  # Импортируем декоратор
from django.http import JsonResponse
from .forms import LoginForm, RegisterForm
from .models import Note


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

            user = form.save(commit=False)  # Создаём пользователя, но не сохраняем в базе
            user.set_password(form.cleaned_data['password'])  # Устанавливаем пароль
            user.save()  # Сохраняем пользователя в базе данных
            login(request, user)  # Автоматически авторизуем пользователя

            return redirect('notes')

    else:
        form = RegisterForm()  # Пустая форма при GET-запросе

    return render(request, 'pages/registration.html', {'form': form})


@login_required
def notes(request):

    # Получаем все заметки текущего пользователя
    user_notes = Note.objects.filter(user=request.user)

    return render(request, 'pages/notes.html', {'notes': user_notes})


@login_required
def create_note(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            note = Note.objects.create(user=request.user, text=text)
            return JsonResponse({
                'status': 'success',
                'message': 'Заметка создана',
                'note': {
                    'id': note.id,
                    'text': note.text
                }
            })
        return JsonResponse({'status': 'error', 'message': 'Текст заметки не может быть пустым'})

    return JsonResponse({'status': 'error', 'message': 'Неверный запрос'})


@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            note.text = text
            note.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Заметка обновлена',
                'note': {
                    'id': note.id,
                    'text': note.text
                }
            })
        return JsonResponse({'status': 'error', 'message': 'Текст заметки не может быть пустым'})
    return JsonResponse({'status': 'error', 'message': 'Неверный запрос'})


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        note.delete()
        return JsonResponse({'status': 'success', 'message': 'Заметка удалена'})
    return JsonResponse({'status': 'error', 'message': 'Неверный запрос'})