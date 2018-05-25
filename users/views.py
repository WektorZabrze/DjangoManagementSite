from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
from django.shortcuts import render, redirect

from chat.models import ChatRoom
from .forms import PersonForm, PersonChangeForm
from .utils import calculate_productivity_index


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
    subordinates = request.user.subordinates.all()
    form = PersonChangeForm
    return render(request, 'user_views/edit.html', locals())
