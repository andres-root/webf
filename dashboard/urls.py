from django.conf.urls import *


urlpatterns = patterns('dashboard.views',
    url(r'^dashboard/$', 'index', name='dashboard_index'),
    url(r'^dashboard/calendar/$', 'calendar', name='dashboard_calendar'),
    url(r'^dashboard/reviews/$', 'reviews', name='dashboard_reviews'),
    url(r'^dashboard/invoices/$', 'invoices', name='dashboard_invoices'),
    url(r'^dashboard/invoices/x/$', 'invoice', name='dashboard_invoice'),
    url(r'^dashboard/inbox/$', 'conversations', name='dashboard_conversations'),
    url(r'^dashboard/conversation/(\d+)/$', 'messages', name='dashboard_messages'),
    url(r'^dashboard/verification/$', 'verification', name='dashboard_verification'),
    url(r'^spaces/$', 'space', name='profile_space'),
)
