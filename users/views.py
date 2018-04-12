from django.shortcuts import render
from django.http import HttpResponse
from users.models import Person

def display_users(request):
	list_of_users = Person.objects.all()
	printed = "<html><body><br> </body></html>".join([str(i) for i in list_of_users])
	html = "<html><body>List of users:<br> %s.</body></html>" % printed
	return HttpResponse(html)

	


# Create your views here.
