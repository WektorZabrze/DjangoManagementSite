# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Person

class PersonCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Person
        fields = ['username', 'email', 'first_name', 'surname', 'age', 'position']
        


class PersonChangeForm(UserChangeForm):

    #class Meta(#UserChangeForm.Meta):
    class Meta():
        model = Person
       	fields = PersonCreationForm.Meta.fields #+ 'task_ids' + 'subordinate_ids'
