from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^login/$', views.login_user ),
	url (r'^logout/', views.logout_user),
	url(r'^recruit/', views.recruit),
	url(r'', views.index),
]