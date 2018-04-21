from .models import Task
import django_filters
#pip install django-filter


#Faplo - still working 14.04
#TO DO: DateRangeFilter, displaying data
class TaskFilter(django_filters.FilterSet):
    #case insensensetive search and if contains mentioned part
    task_name = django_filters.CharFilter(lookup_expr='icontains')
    task_description = django_filters.CharFilter(lookup_expr='icontains')
    date_null = django_filters.BooleanFilter(name='deadline_date', label="Is deadline set?", lookup_expr='isnull')
    #below options are temporary
    created_date__gt = django_filters.NumberFilter(name='created_date', lookup_expr='year__gt')
    created_date__lt = django_filters.NumberFilter(name='created_date', lookup_expr='year__lt')
    #created_date = django_filters.DateFromToRangeFilter() #doesnt work
    class Meta:
        model = Task
        exclude = ['created_date', 'deadline_date', ]