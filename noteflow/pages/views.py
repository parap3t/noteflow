from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required  # Импортируем декоратор
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
                return redirect('home')  # Перенаправление после входа
            else:
                form.add_error(None, 'Неверный логин или пароль')
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
            return redirect('home')  # Перенаправляем на главную страницу
    else:
        form = RegisterForm()  # Пустая форма при GET-запросе

    return render(request, 'pages/register.html', {'form': form})


@login_required
def notes(request):

    # Получаем все заметки текущего пользователя
    user_notes = Note.objects.filter(user=request.user)

    return render(request, 'pages/notes.html', {'notes': user_notes})