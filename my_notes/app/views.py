from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Note, User
from .forms import NoteForm, UserRegister
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout as auth_logout
from django.core.paginator import Paginator



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
                User.objects.create(name=username, password=hashed_password)
                return redirect('note_list')


        info['form'] = form
    else:
        form = UserRegister()

    info['form'] = form
    return render(request, 'app/register.html', info)





def logout(request):
    auth_logout(request)
    return redirect('register')



def note_list(request):
    notes_list = Note.objects.all().order_by('-created_at')
    paginator = Paginator(notes_list, 4)  # 5 заметок на странице
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

# Create your views here.



#


# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('note_list')
#     else:
#         form = UserCreationForm()
#     return render(request, 'app/register.html', {'form': form})
#
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('note_list')
#     return render(request, 'app/login.html')