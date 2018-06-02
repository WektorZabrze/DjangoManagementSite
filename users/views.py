from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
from users.models import Person
from chat.models import ChatRoom
from django.template import Context, loader
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required
from tasks.models import Task
from .forms import PersonForm, PersonChangeForm, ChoiceForm
from chat.models import ChatRoom
from .forms import PersonForm, PersonChangeForm
from .utils import calculate_productivity_index
from queue import Queue as Queue


# modified by Faplo 30.04 for chat purposes
def index(request):
    return render(request, 'user_views/uniformed_view.html', locals())


@login_required
def chat(request):
    chat_rooms = ChatRoom.objects.order_by("room_name")
    return render(request, 'chat/chat.html', locals())


@login_required
def logout_user(request):
    return logout(request)


def login_user(request):
    if not request.user.is_authenticated:
        return login(request)
    else:
        return redirect('/')


@login_required
def productivity_index(request):
    p_index = request.user.productivity_index = calculate_productivity_index(request.user.personal_id)
    return render(request, 'user_views/productivity_index.html', locals())


@login_required
def recruit(request):
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save()
            person.save()
            request.user.subordinates.add(person)
            return redirect('/')
    else:
        form = PersonForm()
    return render(request, 'user_views/recruit.html', {'form': form})


def edit(request):
    if request.method == 'POST':
        return HttpResponse('{}'.format(request.POST.get('choice_field')))
    else:
        subordinates = request.user.subordinates.all()
        choice_list = []
        for item in subordinates:
            choice_list.append(('{}'.format(item),'{}'.format(item)))
        form = ChoiceForm(choice_list)
        return render(request, 'user_views/edit.html', locals())



@login_required
def plot_graph(request):
    root = Person.objects.get(position="BOS")
    persons_queue = Queue()
    persons_queue.put(root)
    string = "digraph {\n"
    while not persons_queue.empty():
        actual = persons_queue.get()
        for i in actual.subordinates.all():
            string += "{} -> {};\n".format(str(actual), str(i))
            persons_queue.put(i)
    string += "}"
    return HttpResponse(string)