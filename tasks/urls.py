from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.tasks_list, name='tasks_list'),
    url(r'add/$', views.TaskCreate.as_view(), name='task-add'),
]