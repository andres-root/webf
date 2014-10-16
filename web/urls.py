from django.conf.urls import *

urlpatterns = patterns('web.views',
    url(r'^$', 'index', name='index'),
    url(r'^search/$', 'search', name='search'),
    # url(r'^signin/$', 'signin', name='signin'),
    url(r'^continue/$', 'continueReg', name='continueReg'),
    url(r'^signup/$', 'signup', name='signup'),
    # url(r'^signout/$', 'signout', name='signout'),
    url(r'^signup/step-2$', 'signup3', name='signup3'),
    url(r'^signup/final-step$', 'signup2', name='signup2'),
    url(r'^trainer/(?P<id>.*)$', 'trainer', name='trainer'),
    url(r'^book', 'book', name='book'),
    url(r'^review', 'review', name='review'),
    url(r'^profile/(?P<id>.*)$', 'profile', name='profile'),
    url(r'^profile/calendar$', 'profileCalendar', name='profileCalendar'),
    url(r'^profile/info$', 'profileInfo', name='profileInfo'),

    # Messages
    url(r'^messages/$', 'messages', name='messages'),
)
