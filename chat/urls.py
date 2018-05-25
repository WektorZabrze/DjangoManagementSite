from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.chat_list, name='chat_list'),
    url(r'add/$', views.chat_add, name='chat_add'),
    url(r'end/(?P<pk>\d+)/$', views.chat_remove, name='chat_remove'),
    url(r'(?P<pk>\d+)/$', views.chat_view, name='chat_view'),
]