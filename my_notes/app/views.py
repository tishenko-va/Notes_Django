from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, User
from .forms import NoteForm, UserRegister, UserLogin
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.contrib.auth import logout as auth_logout


def register(request):
    info = {}
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']

            if password != repeat_password:
                info['error'] = 'Пароли не совпадают'
            else:
                hashed_password = make_password(password)
                User.objects.create(username=username,
                                    password=hashed_password)  # Исправлено: имя поля должно быть username
                return redirect('note_list')

        info['form'] = form
    else:
        form = UserRegister()

    info['form'] = form
    return render(request, 'app/register.html', info)


def login_view(request):
    info = {}
    if request.method == 'POST':
        form = UserLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.all()
            for u in user:
                if user is not None:
                    return redirect('note_list')
                else:
                    info['error'] = 'Неверное имя пользователя или пароль'
    else:
        form = UserLogin()

    info['form'] = form
    return render(request, 'app/login.html', info)


def logout(request):
    auth_logout(request)
    return redirect('register')


def logout(request):
    auth_logout(request)
    return redirect('register')


def login_view(request):
    info = {}
    if request.method == 'POST':
        form = UserLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.all()
            for u in user:
                if user is not None:
                    return redirect('note_list')
                else:
                    info['error'] = 'Неверное имя пользователя или пароль'
    else:
        form = UserLogin()

    info['form'] = form
    return render(request, 'app/login.html', info)


def logout(request):
    auth_logout(request)
    return redirect('register')


def note_list(request):
    notes_list = Note.objects.all().order_by('-created_at')
    paginator = Paginator(notes_list, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'app/note_list.html', {'notes': page_obj})


def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'app/note_form.html', {'form': form})


def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'app/note_form.html', {'form': form})


def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'app/delete.html', {'note': note})
