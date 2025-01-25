from django.contrib import admin
from .models import Note, CustomUser

admin.site.register(Note)
admin.site.register(CustomUser)
# username: admin
# em: valera@gmail.com
# pass: 12345678
