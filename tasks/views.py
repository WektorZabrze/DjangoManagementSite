from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task


# Faplo - currently working 14.04
@login_required
def tasks_list(request):
    tasks_table = Task.objects.all();
    return render(request, 'tasks/tasks_list.html', locals())


# Faplo - currently working 14.04
@login_required
def search_task(request):
    tasks_table = Task.objects.all()
    tasks_filter = TaskFilter(request.GET, queryset=tasks_table)
    return render(request, 'tasks/task_search.html', {'filter': tasks_filter})


# Marcin changed 19.04 and working
@login_required
def task_add(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            task.save()
            return redirect('tasks_list')
    else:
        form = TaskForm(request = request)
    return render(request, 'tasks/task_form.html', {'form': form})


# Marcin 19.04 and working
@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            task.save()
            return redirect('tasks_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_edit.html', {'form': form})


@login_required
def user_tasks(request):
    tasks_table = Task.objects.filter(assigned_employee=request.user)
    return render(request, 'tasks/user_tasks.html', locals())