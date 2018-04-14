from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Person
from django import forms

from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.contrib.auth.models import Group


class PersonCreationForm(forms.ModelForm):
	password = forms.CharField(label = "Password", widget = forms.PasswordInput)
	password_confirm = forms.CharField(label = "Confirm password", widget = forms.PasswordInput)

	class Meta:
		model = Person
		fields = ('username', 'email', 'first_name', 'surname', 'date_of_birth', 'position')

	def check_password_match (self):
		password = self.cleaned_data.get("password")
		password_confirm = self.cleaned_data.get("password_confirm")

		if password and password_confirm and password != password_confirm:
			raise forms.ValidationError("Passwords dont't match")
		return password_confirm

	def save(self, commit = True):
		user = super().save(commit = False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user


class PersonChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = Person
		fields = ('username', 'email', 'first_name', 'surname', 'date_of_birth', 'position', 'is_admin')

	def clean_password(self):
		return self.initial["password"]

class PersonAdmin(BaseUserAdmin):
	form = PersonChangeForm
	add_form = PersonCreationForm

	list_display = ('username', 'email', 'first_name', 'surname', 'date_of_birth', 'position', 'is_admin')
	list_filter = ("is_admin",)
	fieldsets = (
		(None, {"fields" : ('email', 'password')}),
		('Personal info', { 'fields': ('username', 'email', 'first_name', 'surname', 'date_of_birth', 'position',)}),
		('Permitions', {'fields' : ('is_admin',)}),
	)

	add_fieldsets = (
		(None, {
			'classes' : ('wide',),
			'fields' : ('username', 'email', 'first_name', 'surname', 'date_of_birth', 'position', 'password', 'password_confirm')
			}),
	)

	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal= ()

admin.site.register(Person, PersonAdmin)
admin.site.unregister(Group)