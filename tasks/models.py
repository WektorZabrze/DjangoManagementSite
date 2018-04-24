from django.db import models
from users.models import Person
from django.utils import timezone
from model_utils import Choices

#we're gonna stick to it for now - Faplo 13.04.2018
class Task(models.Model):
    #(database value, code-readable value, human-readable value)
    #maybe modify values names so the code-readable and human-readable values won't be mistaken - Faplo
    PRIORITY_VALUES = Choices(
        (1, 'low', "Low"),
        (2, 'medium', 'Medium'),
        (3, 'high', 'High'),
        (4, 'critical', 'Critical'),
    )

    assigned_employee = models.ForeignKey(Person, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100)
    task_description = models.TextField()
    priority = models.IntegerField(default=PRIORITY_VALUES.medium, choices = PRIORITY_VALUES)
    created_date = models.DateTimeField(
            default=timezone.now)
    deadline_date = models.DateTimeField(
            blank=True, null=True)

    def __str__(self):
        return self.task_name
    
    def get_absolute_url(self):
        return "/tasks/"
