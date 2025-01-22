from django.db import models


class User(models.Model):
    pass
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=20, default='default_password')


class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title
