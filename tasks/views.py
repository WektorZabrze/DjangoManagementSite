from .models import Task
from .filters import TaskFilter
from django.shortcuts import render
from django.views.generic.edit import CreateView



#Faplo - currently working 14.04
def tasks_list(request):
    tasks_table = Task.objects.all();
    return render(request, 'tasks/tasks_list.html', locals())

#Faplo - currently working 14.04
def search_task(request):
    tasks_table = Task.objects.all()
    tasks_filter = TaskFilter(request.GET, queryset=tasks_table)
    return render(request, 'tasks/task_search.html', {'filter': tasks_filter})

#Marcin
class TaskCreate(CreateView):
    model = Task
    fields = ['assigned_employee', 'task_name', 'task_description', 'priority', 'created_date', 'deadline_date']