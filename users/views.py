from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.models import Person
from chat.models import ChatRoom
from django.template import Context, loader
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required
from tasks.models import Task
from .forms import PersonForm, PersonChangeForm

#modified by Faplo 30.04 for chat purposes
def index(request):
    chat_rooms = ChatRoom.objects.order_by("room_name")
    return render(request, 'user_views/uniformed_view.html', locals())

@login_required
def logout_user(request):
	return logout(request)

def login_user(request):
	if not request.user.is_authenticated:
		return login(request)
	else:
		return redirect('/')

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
    subordinates = request.user.subordinates.all()
    form = PersonChangeForm
    return render(request, 'user_views/edit.html', locals())
