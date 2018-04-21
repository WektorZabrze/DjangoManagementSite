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
	return render(request, 'user_views/uniformed_view.html')


def logout_user(request):
	return logout(request)

def login_user(request):
	if not request.user.is_authenticated:
		return login(request)
	else:
		return index(request)