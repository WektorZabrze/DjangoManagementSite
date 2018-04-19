from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.tasks_list, name='tasks_list'),
    url(r'add/$', views.task_add, name='task-add'),
    url(r'search/$', views.search_task, name='task-search'),
]
