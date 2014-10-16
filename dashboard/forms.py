from django import forms
from dashboard.models import Session


class session_form(forms.ModelForm):

    class Meta:
        model = Session
        exclude = ('id', 'date_created', 'active', 'deleted', 'trainer')
