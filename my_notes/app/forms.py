from django import forms
from .models import Note

class UserRegister(forms.Form):
    username = forms.CharField(max_length=30, required=True, label='Введите логин')
    password = forms.CharField(min_length=8, label="Введите пароль", widget=forms.PasswordInput, required=True )
    repeat_password = forms.CharField(min_length=8, label='Повторите пароль', widget=forms.PasswordInput, required=True)

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']