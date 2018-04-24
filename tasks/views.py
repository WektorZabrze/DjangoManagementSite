from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from .text_dimensionality_reduction import textdimensionalityreduction

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task

#TEMPORARY
from .load_sentences_to_model import loading

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

#temporary - for loading tasks from file to model
def loading_to_model_tmp(request):
    loading()
    return render(request, 'tasks/task_search.html')



@login_required
def task_add(request):
    if request.method == "POST":
        form = TaskForm(request.POST, request = request)
        if form.is_valid():
            task = form.save()
            task.save()
            return redirect('/')
    else:
        form = TaskForm(request = request)
    return render(request, 'tasks/task_form.html', {'form': form})


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
	tasks_table_subordinates =Task.objects.filter(assigned_employee__in = request.user.subordinates.all())
	return render(request, 'tasks/user_tasks.html', locals())

def get_chart(request):
    return render(request, 'tasks/chart/chart.html')


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        # example, temporary values
        chartValuesDictionary = textdimensionalityreduction.sentencesTo2D()
        x_values = chartValuesDictionary["x"]
        y_values = chartValuesDictionary["y"]
        tasks_descriptions = chartValuesDictionary["labels"]
        # to do - assign color of point by priority

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
