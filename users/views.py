from django.shortcuts import render
from django.http import HttpResponse
from users.models import Person

def display_users(request):
	list_of_users = Person.objects.all()
	printed = "<html><body><br> </body></html>".join([str(i) for i in list_of_users])
	html = "<html><body>List of users:<br> {}.</body></html>".format(printed)
	return HttpResponse(html)

def index(request):
	if not request.user.is_authenticated:
		return default_view()
	elif request.user.position == 'BOS':
		return boss_view()
	elif request.user.position:
		return whatever()
	else:
		return default_view()

def boss_view():
	return HttpResponse("<html><body><h1> Hello BOSS! </h1></body></html>")

def default_view():
	url = 'http://localhost:8000/login/'
	return HttpResponse("<html><body><h1><a href={} targer=\"_blank\"> Login here </a></h1></body></html>".format(url))

def whatever():
	return HttpResponse("<html><body> You are logged in!</html><body>")

