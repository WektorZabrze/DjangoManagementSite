from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^productivity_index/$', views.productivity_index ),
	url(r'^login/$', views.login_user ),
	url (r'^logout/', views.logout_user),
	url (r'^graph/', views.plot_graph),
	url(r'^recruit/', views.recruit),
	url(r'^edit2/', views.edit2, name="edit2"),
	url(r'^edit/', views.edit),
	url(r'^chat/', views.chat),
	url(r'', views.index),
]