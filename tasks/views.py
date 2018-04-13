from .models import Task
from django.shortcuts import render


#it was previously  name display_tasks - I think current name is better because we can see with wich template it's related - Faplo
def tasks_list(request):
    tasks_table = Task.objects.all();
    return render(request, 'tasks/tasks_list.html', locals())
