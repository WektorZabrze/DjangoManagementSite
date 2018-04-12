from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import PersonCreationForm, PersonChangeForm
from .models import Person

class PersonAdmin(admin.ModelAdmin):
    add_form = PersonCreationForm
    form = PersonChangeForm
    model = Person
    list_display = ['email', 'username', 'first_name', 'surname', 'age', 'position']


admin.site.register(Person, PersonAdmin)