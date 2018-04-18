from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.models import Person
from django.template import Context, loader
from django.contrib.auth.views import login, logout

def display_users(request):
	list_of_users = Person.objects.all()
	printed = "<br>".join([str(i) for i in list_of_users])
	html = "<html><body>List of users:<br> {}.</body></html>".format(printed)
	return HttpResponse(html)

def index(request):
	if not request.user.is_authenticated:
		return default_view()
	elif request.user.position == 'BOS':
		return boss_view()
	elif request.user.position == 'MAN':
		return manager_view()
	elif request.user.position == 'SUP':
		return supervisor_view()
	elif request.user.position == 'WOR':
		return worker_view()	
	elif request.user.position:
		return whatever()
	else:
		return default_view()

def boss_view():
	return HttpResponse(loader.get_template("user_views/boss_view.html").render())

def manager_view():
	return HttpResponse(loader.get_template("user_views/manager_view.html").render())

def supervisor_view():
	return HttpResponse(loader.get_template("user_views/supervisor_view.html").render())

def worker_view():
	return HttpResponse(loader.get_template("user_views/worker_view.html").render())

def default_view():
	return HttpResponse(loader.get_template("user_views/default_view.html").render())
	

def whatever():
	return HttpResponse("<html><body> You are logged in!</html><body>")

def logout_user(request):
	return logout(request)

def login_user(request):
	if not request.user.is_authenticated:
		return login(request)
	else:
		return index(request)