from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from rest_framework.views import APIView

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
            task = form.save()
            task.save()
            return redirect('tasks_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


# Marcin 19.04 and working
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


def get_chart(request):
    return render(request, 'tasks/chart/chart.html')


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        # example, temporary values
        x_values = [1, 2, 3, 4, 5, 6, 7, 8]
        y_values = [1, 2, 3, 4, 5, 6, 7, 8]
        tasks_descriptions = ["task desc 1", "task desc 2", "task desc 3", "task desc 4", "task desc 5", "task desc 6",
                              "task desc 7", "task desc 8"]

        #Here we need to build proper JSON structure as Chart.js we use require such
        all_tasks_chart_data = []
        for i in range(len(x_values)):
            chart_point_settings = []
            chart_point_settings.append({"x": x_values[i],
                                         "y": y_values[i],
                                         "r": 15})
            single_task_data = {
                "label": tasks_descriptions[i],
                "data": chart_point_settings,
                "backgroundColor": "rgba(255,221,50,0.2)",
                "borderColor": "rgba(255,221,50,1)",
            }
            all_tasks_chart_data.append(single_task_data)

        return JsonResponse({
            "tasks_data": all_tasks_chart_data
        })
