from django.conf.urls import url
from . import views

from .filters import TaskFilter
from django_filters.views import FilterView

urlpatterns = [
    url(r'^$', views.tasks_list, name='tasks_list'),
    url(r'add/$', views.TaskCreate.as_view(), name='task-add'),
    url(r'search/$', views.search_task, name='task-search'),
]