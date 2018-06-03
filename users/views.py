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
from .forms import PersonForm, PersonChangeForm, ChangeForm
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

@login_required
def edit2(request):
	if request.session['to_edit'] == None:
		return redirect('/')
	to_edit = Person.objects.get(personal_id = request.session['to_edit'])
	choice_dict = subordinates_dictionary(request)
	form = ChangeForm(to_edit = to_edit, choice_dict = choice_dict)
	if request.method == 'POST':
		if request.POST.get('username'):
			to_edit.username = request.POST.get('username')
		if request.POST.get('email'):
			to_edit.first_name = request.POST.get('email')
		if request.POST.get('first_name'):
			to_edit.first_name = request.POST.get('first_name')
		if request.POST.get('surname'):
			to_edit.surname = request.POST.get('surname')
		if request.POST.get('date_of_birth'):
			to_edit.date_of_birth = request.POST.get('date_of_birth')
		if request.POST.get('position'):
			to_edit.position = request.POST.get('position')
		if request.POST.get('subordinates'):
			to_edit.subordinates.set(request.POST.get('subordinates'))
		to_edit.save()
		request.session['to_edit'] = None
		return redirect('/')
	else:
		return render(request, 'user_views/edit.html', locals())

@login_required
def edit(request):
    if request.method == 'POST':
    	to_edit = Person.objects.get(personal_id = request.POST.get('Subordinates'))
    	personal_id = int(to_edit.personal_id)
    	request.session['to_edit'] = personal_id
    	return redirect('edit2')
    else:
        choice_dict = subordinates_dictionary(request)
        form = ChoiceForm(choice_dict)
        return render(request, 'user_views/edit.html', locals())


def subordinates_dictionary(request):
	subordinates = request.user.subordinates.all()
	choice_dict = []
	for item in subordinates:
		choice_dict.append(('{}'.format(item.personal_id),'{}'.format(item)))
	return choice_dict