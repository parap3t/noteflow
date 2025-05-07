from django.db import models
from django.contrib.auth.models import User  # Подключаем встроенную модель User


class Note(models.Model):
    text = models.TextField()  # Поле для текста заметки
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Внешний ключ к пользователю


