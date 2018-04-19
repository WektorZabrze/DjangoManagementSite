from django.shortcuts import redirect
from django.shortcuts import render

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task


# Faplo - currently working 14.04
def tasks_list(request):
    tasks_table = Task.objects.all();
    return render(request, 'tasks/tasks_list.html', locals())


# Faplo - currently working 14.04
def search_task(request):
    tasks_table = Task.objects.all()
    tasks_filter = TaskFilter(request.GET, queryset=tasks_table)
    return render(request, 'tasks/task_search.html', {'filter': tasks_filter})


# Marcin changed 19.04 and working
def task_add(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('tasks_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})
