from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):

    username = forms.CharField(label='Логин', max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'required': 'required'
    }))

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'required': 'required'
    }))

    confirm_password = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'confirm_password',
        'required': 'required'
    }))

    class Meta:

        model = User
        fields = ['username']

    def clean_username(self):

        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким именем уже существует.')

        return username


    def clean(self):

        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Пароли не совпадают')


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'required': 'required'
    }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'required': 'required'
    }))
