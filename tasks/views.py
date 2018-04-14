from .models import Task
from django.shortcuts import render
from django.views.generic.edit import CreateView



#it was previously  name display_tasks - I think current name is better because we can see with wich template it's related - Faplo
def tasks_list(request):
    tasks_table = Task.objects.all();
    return render(request, 'tasks/tasks_list.html', locals())


class TaskCreate(CreateView):
    model = Task
    fields = ['assigned_employee', 'task_name', 'task_description', 'priority', 'created_date', 'deadline_date']