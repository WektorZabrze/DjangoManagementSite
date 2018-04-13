from django.db import models
from users.models import Person

# Create your models here.


class Task(models.Model):
    task_description = models.CharField(max_length=1000, default="")
    post_date = models.CharField(max_length=100, default="")
    deadline = models.CharField(max_length=100, default="")
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_description
