from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Todo(models.Model):
    title = models.TextField(max_length=25)
    text = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):

        return f"{self.id}-{self.title}-{self.created}({self.user.username})"
