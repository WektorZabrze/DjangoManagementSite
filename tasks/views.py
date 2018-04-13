from .models import Task
from django.shortcuts import render

# Create your views here.


def display_tasks(request):
    all_tasks = Task.objects.all()
    return render(request, 'tasks/index.html', {'all_tasks': all_tasks})
