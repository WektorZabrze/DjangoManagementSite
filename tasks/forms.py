from django import forms

from .models import Task


# Marcin working 19.04
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['assigned_employee', 'task_name', 'task_description', 'priority', 'created_date', 'deadline_date']
