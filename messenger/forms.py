from django import forms
from messenger.models import Message


class message_form(forms.ModelForm):

    class Meta:
        model = Message
        exclude = ('id', 'conversation', 'date_created', 'date_deleted', 'active', 'deleted', 'seen', 'sender', 'receiver')
