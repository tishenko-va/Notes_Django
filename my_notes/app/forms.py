from django import forms
from .models import Note, User
from django import forms


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']


class UserRegister(forms.Form):
    username = forms.CharField(max_length=30, required=True, label='Введите логин')
    password = forms.CharField(min_length=8, label="Введите пароль", widget=forms.PasswordInput, required=True)
    repeat_password = forms.CharField(min_length=8, label='Повторите пароль', widget=forms.PasswordInput, required=True)


class UserLogin(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=150)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
