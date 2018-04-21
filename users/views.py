from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.models import Person
from django.template import Context, loader
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required


def index(request):
	return render(request, 'user_views/uniformed_view.html')

@login_required
def logout_user(request):
	return logout(request)

def login_user(request):
	if not request.user.is_authenticated:
		return login(request)
	else:
		return index(request)