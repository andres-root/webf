# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import smart_unicode
from authsys.models import User


class State(models.Model):
    """
    STATE
    """
    name = models.CharField(max_length=200, null=False, blank=False)
    code = models.CharField(max_length=220, null=True, blank=True)
    active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_updated = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __unicode__(self):
        return smart_unicode(self.code)


class City(models.Model):
    """
    CITY
    """
    name = models.CharField(max_length=200, null=False, blank=False)
    code = models.CharField(max_length=220, null=True, blank=True)
    active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_updated = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __unicode__(self):
        return smart_unicode(self.name)


class Review(models.Model):
    """
    Review
    """
    id_sender = models.ForeignKey(User, related_name='review_sender')
    id_receiver = models.ForeignKey(User, related_name='review_receiver')
    content = models.TextField(max_length=1000)
    rating = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_deleted = models.DateTimeField(blank=True, null=True,
                                        auto_now_add=False, auto_now=False)

    def __unicode__(self):
        return smart_unicode(self.content)


class Speciality(models.Model):
    """
    Speciality
    """
    name = models.CharField(max_length=120, null=False, blank=False)
    description = models.CharField(max_length=1000, null=True, blank=True)
    active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_updated = models.DateTimeField(auto_now_add=True, auto_now=True)


class UserProfile(models.Model):
    """
    Client Profile
    """
    user = models.OneToOneField(User)
    date_birth = models.DateField(null=False, blank=False)
    genre = models.CharField(max_length=2, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    id_state = models.OneToOneField(State, null=True, blank=True)
    id_city = models.OneToOneField(City, null=True, blank=True)
    zip_code = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=1000, null=True, blank=True)
    is_trainer = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_updated = models.DateTimeField(auto_now_add=True, auto_now=True)
    date_deleted = models.DateTimeField(blank=True, null=True,
                                        auto_now_add=False, auto_now=False)

    def __unicode__(self):
        return smart_unicode(self.user.username)


class TrainerProfile(models.Model):
    """
    Trainer Profile
    """
    user = models.OneToOneField(User)
    date_birth = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=2, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    #id_state = models.IntegerField(default=1, null=True, blank=True)
    id_state = models.ForeignKey(State, null=True, blank=True)
    #id_city = models.IntegerField(default=1, null=True, blank=True)
    id_city = models.ForeignKey(City, null=True, blank=True)
    zip_code = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=1000, null=True, blank=True)
    specialities = models.CharField(max_length=10000, null=False, blank=False)
    payment_method = models.CharField(max_length=200, null=True, blank=True)
    charge = models.FloatField(null=True, blank=True)
    rate = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_updated = models.DateTimeField(auto_now_add=True, auto_now=True)
    date_deleted = models.DateTimeField(blank=True, null=True,
                                        auto_now_add=False, auto_now=False)

    def __unicode__(self):
        return smart_unicode(self.user.username)
