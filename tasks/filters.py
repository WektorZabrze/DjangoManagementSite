from .models import Task
import django_filters


class TaskFilter(django_filters.FilterSet):
    task_name = django_filters.CharFilter(lookup_expr='icontains')
    task_description = django_filters.CharFilter(lookup_expr='icontains')
    date_null = django_filters.BooleanFilter(name='deadline_date', label="Is deadline set?", lookup_expr='isnull')
    created_date__gt = django_filters.NumberFilter(name='created_date', lookup_expr='year__gt')
    created_date__lt = django_filters.NumberFilter(name='created_date', lookup_expr='year__lt')
    class Meta:
        model = Task
        exclude = ['created_date', 'deadline_date', ]