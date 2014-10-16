# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Q

from dashboard.forms import session_form

from messenger.models import Conversation, Message


def index(request):
    if request.user.is_authenticated():
        user = request.user
        ctx = {}
        return render_to_response('dashboard/home.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


def calendar(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = session_form(request.POST)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect('dashboard/calendar')
        ctx = {}
        ctx['form'] = session_form
        return render_to_response('dashboard/calendar.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


def reviews(request):
    if request.user.is_authenticated():
        user = request.user
        ctx = {}
        return render_to_response('dashboard/reviews.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


def invoices(request):
    if request.user.is_authenticated():
        user = request.user
        ctx = {}
        return render_to_response('dashboard/invoices.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


def invoice(request):
    if request.user.is_authenticated():
        user = request.user
        ctx = {}
        return render_to_response('dashboard/invoice.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


def conversations(request):
    if request.user.is_authenticated():
        user = request.user
        conversations = Conversation.objects.filter(Q(receiver=user.id) | Q(sender=user.id))
        ctx = {'conversations': conversations}
        return render_to_response('dashboard/conversations.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


def messages(request, id):
    if request.user.is_authenticated():
        conversation = Conversation.objects.get(pk=id)
        messages = Message.objects.filter(conversation=id)
        ctx = {}
        ctx['messages'] = messages
        ctx['conversation'] = conversation
        return render_to_response('dashboard/messages.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


def verification(request):
    if request.user.is_authenticated():
        user = request.user
        ctx = {}
        return render_to_response('dashboard/verification.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


def space(request):
    if request.user.is_authenticated():
        user = request.user
        ctx = {}
        return render_to_response('profile/space.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')
