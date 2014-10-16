from django.conf.urls import *

urlpatterns = patterns('messenger.views',
        url(r'^create/', 'create_conversation', name='create_conversation'),
        url(r'^send/$', 'send_message', name='send_message'),
)
