from django import forms

from .models import Person

class PersonForm(forms.ModelForm):
	password = forms.CharField(label = "Password", widget = forms.PasswordInput)
	password_confirm = forms.CharField(label = "Confirm password", widget = forms.PasswordInput)
	class Meta:
		model = Person
		fields = ('username', 'email', 'first_name', 'surname', 'date_of_birth', 'position', 'password')

	def __init__(self, *args, **kwargs):
		super(PersonForm,self).__init__(*args, **kwargs)
		self.fields['username'].help_text = None

	def clean (self):
		cleaned_data = super(PersonForm, self).clean()
		password = self.cleaned_data.get("password")
		password_confirm = self.cleaned_data.get("password_confirm")

		if password and password_confirm and password != password_confirm:
			self.add_error('password_confirm', 'Password does not match.')

	def save(self, commit=True):
		user = super(PersonForm, self).save(commit = False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user


class PersonChangeForm(forms.ModelForm):

	class Meta:
		model = Person
		fields = ('username', 'email', 'first_name', 'surname', 'date_of_birth', 'position', 'subordinates')

class ChoiceForm(forms.ModelForm):
	def __init__(self, _choices):
		super(ChoiceForm, self).__init__()
		self.fields['Subordinates'] = forms.ChoiceField(choices=_choices)

	class Meta:
		model = Person
		fields = ('username',)
		exclude = ('username',)

class ChangeForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		choice_dict = kwargs.pop('choice_dict')
		super(ChangeForm, self).__init__(*args, **kwargs)
		self.fields['username'].help_text = None
		self.fields['username'].initial = kwargs['instance'].username
		self.fields['email'].initial = kwargs['instance'].email
		self.fields['first_name'].initial = kwargs['instance'].first_name
		self.fields['surname'].initial = kwargs['instance'].surname
		self.fields['date_of_birth'].initial = kwargs['instance'].date_of_birth
		if kwargs['instance'].position == "BOS":
			self.fields['position'].initial = 'BOS'
		elif kwargs['instance'].position == "MAN":
			self.fields['position'].initial = 'MAN'
		elif kwargs['instance'].position == "SUP":
			self.fields['position'].initial = 'SUP'
		else:
			self.fields['position'].initial = 'WOR'
		self.fields['subordinates'] = forms.ModelMultipleChoiceField(queryset = choice_dict, )
		self.fields['subordinates'].required = False
		

	class Meta:
		model = Person
		fields = ('username', 'email', 'first_name', 'surname', 'date_of_birth', 'position', 'subordinates')
