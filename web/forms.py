# -*- coding: utf-8 -*-
from django import forms
from authsys.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from web.models import UserProfile, TrainerProfile, Review


class SignupForm(ModelForm):
    class Meta:
        model = User
        fields = ['is_trainer', 'username', 'email', 'password', 'first_name', 'last_name']


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class signinForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))


class BookForm(forms.Form):
    people = forms.CharField(widget=forms.TextInput())
    sessions = forms.CharField(widget=forms.TextInput())
    message = forms.CharField(widget=forms.Textarea())

    def clean(self):
        return self.cleaned_data


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['is_trainer', 'active', 'deleted', 'date_created', 'date_updated', 'date_deleted']


class TrainerForm(ModelForm):
    class Meta:
        model = TrainerProfile
        exclude = ['active', 'deleted', 'date_created', 'date_updated', 'date_deleted']


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        exclude = ['id_sender', 'id_receiver', 'rating', 'active', 'deleted', 'date_created', 'date_deleted']
