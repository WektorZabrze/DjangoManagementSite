from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.tasks_list, name='tasks_list'),
    url(r'chart/menu/$', views.chart_menu, name='chart_menu'),
    url(r'choose/$', views.choose_task, name="choose_task"),
    url(r'choose_edit/$', views.choose_task_edit, name = "choose_task_edit"),
    url(r'menu/$', views.task_menu, name = 'task_menu'),
    url(r'add/$', views.task_add, name='task-add'),
    url(r'search/$', views.search_task, name='task-search'),
    url (r'^user_tasks/', views.user_tasks),
    url(r'edit/(?P<pk>\d+)/$', views.task_edit, name='task-edit'),
    url(r'api/chart/data/$', views.ChartData.as_view(), name='chart-data'),
    url(r'chart/$', views.get_chart, name='chart-view'),
    url(r'chart/load/$',views.loading_to_model_tmp),
    url(r'chart/remove_result/$',views.remove_dimensionality_reduction_result, name='remove_dimensionality_reduction'),
    url(r'end/(?P<pk>\d+)/$', views.end_task, name='end_task'),
    url(r'revive/(?P<pk>\d+)/$', views.revive_task, name='revive_task'),
    url(r'^(?P<pk>\d+)/$', views.basic_view, name='basic_view'),
]