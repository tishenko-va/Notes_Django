from django.urls import path, include
from .views import note_list, note_create, note_update, note_delete, register, logout

urlpatterns = [
    path('', note_list, name='note_list'),
    path('register/', register, name= 'register'),
    path('create/', note_create, name='note_create'),
    path('update/<int:pk>/', note_update, name='note_update'),
    path('delete/<int:pk>/', note_delete, name='note_delete'),
    path('logout/', logout, name='logout'),

]


