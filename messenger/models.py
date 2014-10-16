from django.db import models
from django.utils.encoding import smart_unicode
from authsys.models import User


class Conversation(models.Model):
    """
    Convesation
    """
    sender = models.ForeignKey(User, related_name='conversationsender_user')
    receiver = models.ForeignKey(User, related_name='conversationreceiver_user')
    seen = models.BooleanField(default=False, null=False, blank=False)
    active = models.BooleanField(default=True, null=False, blank=False)
    deleted = models.BooleanField(default=False, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_deleted = models.DateTimeField(blank=True, null=True, auto_now_add=False, auto_now=False)

    def __unicode__(self):
        return smart_unicode(self.id)


class Message(models.Model):
    """
    Message
    """
    conversation = models.ForeignKey(Conversation, related_name='messagesender_conversation')
    sender = models.ForeignKey(User, related_name='messagesender_user')
    receiver = models.ForeignKey(User, related_name='messagereceiver_user')
    message = models.CharField(max_length=10000, null=False, blank=False)
    seen = models.BooleanField(default=False, null=False, blank=False)
    active = models.BooleanField(default=True, null=False, blank=False)
    deleted = models.BooleanField(default=False, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_deleted = models.DateTimeField(blank=True, null=True, auto_now_add=False, auto_now=False)

    def __unicode__(self):
        return smart_unicode(self.message)
