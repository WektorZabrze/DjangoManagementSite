from django import forms
from users.models import Person
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('users',)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        users = request.user.subordinates.filter()
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['assigned_employee'].queryset = Person.objects.filter(
            personal_id__in=request.user.subordinates.all())
        self.fields['end_date'].widget = forms.HiddenInput()
        self.fields['productivity_index'].widget = forms.HiddenInput()
        if 'instance' in kwargs:
            self.fields['assigned_employee'].initial = kwargs['instance'].assigned_employee
            self.fields['productivity_index'].initial = kwargs['instance'].productivity_index
            self.fields['task_name'].initial = kwargs['instance'].task_name
            self.fields['task_description'].initial = kwargs['instance'].task_description
            self.fields['deadline_date'].initial = kwargs['instance'].deadline_date

class ChooseTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('assigned_employee',)
        exclude = ('assigned_employee',)

    def __init__(self, _choices):
        super(ChooseTaskForm, self).__init__()
        self.fields['Choose task'] = forms.ChoiceField(choices=_choices)