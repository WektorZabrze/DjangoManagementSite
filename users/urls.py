from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^login/$', views.login_user ),
	url (r'^list', views.display_users),
	url (r'^list/', views.display_users),
	url (r'^logout/', views.logout_user),
	url (r'^user_tasks/', views.user_tasks),
	url(r'', views.index),
]