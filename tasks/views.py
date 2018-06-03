import datetime
import json
import os
from pathlib import Path

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from rest_framework.views import APIView

from .filters import TaskFilter
from .forms import TaskForm, ChooseTaskForm
# TEMPORARY
from .load_sentences_to_model import loading
from .models import Task
from .text_dimensionality_reduction import textdimensionalityreduction
from .utils import calculate_productivity_index


@login_required
def basic_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    tae = task.assigned_employee.personal_id
    related_supervisors = [i.personal_id for i in request.user.subordinates.all()]
    if tae == request.user.personal_id or tae in related_supervisors:
        return render(request, 'tasks/basic_view.html', locals())
    else:
        return redirect('tasks_list')


@login_required
def tasks_list(request):
    tasks_table = Task.objects.all();
    return render(request, 'tasks/tasks_list.html', locals())

@login_required
def task_menu(request):
    return render(request, 'tasks/task_menu.html')

@login_required
def chart_menu(request):
    return render(request, 'tasks/chart_menu.html')

@login_required
def search_task(request):
    tasks_table = Task.objects.all()
    tasks_filter = TaskFilter(request.GET, queryset=tasks_table)
    return render(request, 'tasks/task_search.html', {'filter': tasks_filter})


# temporary - for loading tasks from file to model
def loading_to_model_tmp(request):
    loading()
    return render(request, 'tasks/task_search.html')

@login_required
def choose_task(request):
    return choose_task_with_redirect(request, '/tasks/{}/')

@login_required
def choose_task_edit(request):
    return choose_task_with_redirect(request, '/tasks/edit/{}/')

@login_required
def choose_task_with_redirect(request, link):
    if request.method == "POST":
        return redirect(link.format(request.POST.get('Choose task')))
    else:
        tasks_list = []
        for item in Task.objects.filter(assigned_employee = request.user):
            tasks_list.append(("{}".format(item), "{}".format(item)))
        for person in request.user.subordinates.all():
            for item in Task.objects.filter(assigned_employee = person):
                tasks_list.append(("{}".format(item.id), "{}".format(item)))
        form = ChooseTaskForm(tasks_list)
        if tasks_list:
            return render(request, 'user_views/edit.html', locals())
        else:
            return render(request, 'tasks/task_menu.html')

@login_required
def task_add(request):
    if request.method == "POST":
        form = TaskForm(request.POST, request=request)
        if form.is_valid():
            task = form.save()
            task.save()
            return redirect('/tasks/menu/')
    else:
        form = TaskForm(request=request)
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, request=request, instance = task)
        if form.is_valid():
            form.save()
            return redirect('task_menu')
    else:
        form = TaskForm(request=request, instance = task)
    return render(request, 'tasks/task_edit.html', {'form': form})


@login_required
def user_tasks(request):
    tasks_table = Task.objects.filter(assigned_employee=request.user)
    tasks_table_subordinates = Task.objects.filter(assigned_employee__in=request.user.subordinates.all())
    return render(request, 'tasks/user_tasks.html', locals())


def get_chart(request):
    #if there's too little task in the database
    if(len(Task.objects.values("created_date")) < 2):
        return redirect('/')
    return render(request, 'tasks/chart/chart.html')


def end_task(request, pk):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=pk)
        task.end_date = datetime.datetime.now()
        task.productivity_index = calculate_productivity_index(task)
        task.save()
        return render(request, 'tasks/basic_view.html', locals())
    else:
        return redirect('tasks_list')


def revive_task(request, pk):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=pk)
        task.end_date = None
        task.productivity_index = None
        task.save()
        return render(request, 'tasks/basic_view.html', locals())
    else:
        return redirect('tasks_list')


def remove_dimensionality_reduction_result(request):
    jsonFileName = "tasks/chartValueDictionary.json"
    if Path(jsonFileName).is_file():
        os.remove(jsonFileName)
    return redirect("chart_menu")#temporary solution as there's no template for visualization


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        jsonFileName = "tasks/chartValueDictionary.json"
        taskValues = Task.objects.values("created_date")

        newestTask = taskValues.order_by("-created_date")[0]
        nmbOfTasks = len(taskValues)

        recalculateFlag = False

        if Path(jsonFileName).is_file():
            with open(jsonFileName, "r") as file:
                chartValuesDictionary = json.load(file)

                if(str(newestTask["created_date"]) != chartValuesDictionary["newest_task_date"] or
                    nmbOfTasks != chartValuesDictionary["tasks_nmb"]):
                    recalculateFlag = True
        else:
            recalculateFlag = True

        #it is being recalculated if latest task date differs or number of tasks differs
        if recalculateFlag == True:
            chartValuesDictionary = textdimensionalityreduction.sentencesTo2D()
            chartValuesDictionary["newest_task_date"] = str(newestTask["created_date"])
            chartValuesDictionary["tasks_nmb"] = nmbOfTasks
            #save dictionary to file if tasks were modified
            with open(jsonFileName, "w") as file:
                json.dump(chartValuesDictionary,file)

        x_values = chartValuesDictionary["x"]
        y_values = chartValuesDictionary["y"]
        tasks_descriptions = chartValuesDictionary["labels"]
        # to do - assign color of point by priority

        # Here we need to build proper JSON structure as Chart.js we use require such
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
