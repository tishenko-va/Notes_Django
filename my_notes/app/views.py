from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, CustomUser
from .forms import NoteForm, UserRegister, UserLogin
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


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
                CustomUser.objects.create(username=username,
                                          password=hashed_password)
                return redirect('note_list')

        info['form'] = form
    else:
        form = UserRegister()

    info['form'] = form
    return render(request, 'registration/register.html', info)


def login_view(request):
    info = {}
    if request.method == 'POST':
        form = UserLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('note_list')
            else:
                info['error'] = 'Неверное имя пользователя или пароль'
    else:
        form = UserLogin()

    info['form'] = form
    return render(request, 'registration/login.html', info)


def logout(request):
    auth_logout(request)
    return redirect('register')


@login_required
def note_list(request):
    notes_list = Note.objects.filter(author=request.user).order_by('-created_at')
    paginator = Paginator(notes_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'app/note_list.html', {'notes': page_obj})


@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'app/note_form.html', {'form': form})


@login_required
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk, author=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'app/note_form.html', {'form': form})


@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, author=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'app/delete.html', {'note': note})
