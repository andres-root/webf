# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import smart_unicode
from authsys.models import User

from messenger.models import Conversation


class Session(models.Model):
    """
    Session
    """
    trainer = models.ForeignKey(User, related_name='session_trainer')
    people = models.IntegerField(default=1, null=False, blank=False)
    cost = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_deleted = models.DateTimeField(blank=True, null=True,
                                        auto_now_add=False, auto_now=False)

    def __unicode__(self):
        return smart_unicode(self.date)
