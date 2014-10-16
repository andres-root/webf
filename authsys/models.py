# -*- coding:utf-8 -*-
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.utils.encoding import smart_unicode


class User(AbstractUser):
    """
    SystemUser
    """
    def image_path(self, filename):
            path = 'users/img/%s/%s' % (slugify(self.username), str(slugify(filename)))
            return path
    avatar = models.ImageField(upload_to=image_path, blank=True, null=True)
    is_trainer = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        verbose_name = u'User'
        verbose_name_plural = u'Users'

    def __unicode__(self):
        return smart_unicode(self.username)
