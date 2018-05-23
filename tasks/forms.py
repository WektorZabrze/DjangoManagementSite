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
        self.fields['end_date'].initial = None
        self.fields['productivity_index'].initial = None

