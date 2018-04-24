from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.tasks_list, name='tasks_list'),
    url(r'add/$', views.task_add, name='task-add'),
    url(r'search/$', views.search_task, name='task-search'),
    url(r'edit/(?P<pk>\d+)/$', views.task_edit, name='task-edit'),
    url(r'api/chart/data/$', views.ChartData.as_view(), name='chart-data'),
    url(r'chart/$', views.get_chart, name='chart-view'),
    url(r'chart/load/$',views.loading_to_model_tmp),
]
