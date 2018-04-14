from django.conf.urls import url, include
from . import views

urlpatterns = [
	url (r'', include('django.contrib.auth.urls')),
	url (r'^list', views.display_users),
	url (r'^list/', views.display_users),
	url(r'', views.index),
]