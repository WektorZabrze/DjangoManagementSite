from django.db import models
from users.models import Person
from django.utils import timezone

#we're gonna stick to it for now - Faplo 13.04.2018
class Task(models.Model):
    #(database value, code-readable value, human-readable value)
    #maybe modify values names so the code-readable and human-readable values won't be mistaken - Faplo
    priority = models.CharField(max_length = 3, choices =(
		('LOW', 'Low'),
		('MED', 'Medium'),
		('HIG', 'High'),
		('CRI', 'Critical'),
		), default = 'LOW',
	)

    assigned_employee = models.ForeignKey(Person, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100)
    task_description = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    deadline_date = models.DateTimeField(
            blank=True, null=True)

    def __str__(self):
        return self.task_description

    def get_absolute_url(self):
        return "/tasks/"
