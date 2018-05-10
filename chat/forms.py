from django import forms

from .models import ChatRoom


class ChatForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = '__all__'
