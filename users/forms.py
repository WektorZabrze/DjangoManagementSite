from django import forms

from .models import Person

class PersonForm(forms.ModelForm):
	password = forms.CharField(label = "Password", widget = forms.PasswordInput)
	password_confirm = forms.CharField(label = "Confirm password", widget = forms.PasswordInput)
	class Meta:
		model = Person
		fields = ('username', 'email', 'first_name', 'surname', 'date_of_birth','subordinates', 'position', 'password')

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