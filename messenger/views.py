# -*- coding: utf-8 -*-
from authsys.models import User
from django.shortcuts import redirect
from django.http import HttpResponse

from messenger.models import Conversation, Message
from messenger.forms import message_form
from messenger.helpers import send_mail
from custom_decorators.decorators import requires_post, json_response


@requires_post
@json_response
def create_conversation(request):
    form = message_form(request.POST)
    # import ipdb; ipdb.set_trace()
    if form.is_valid():
        try:
            user_sender = User.objects.get(pk=request.POST.get('sender'))
            user_receiver = User.objects.get(pk=request.POST.get('receiver'))
            content = form.cleaned_data['message']
            c = Conversation.objects.create(sender=user_sender, receiver=user_receiver)
            Message.objects.create(conversation=c, sender=user_sender, receiver=user_receiver, message=content)
        # mail_data = {}
        # mail_data['subject'] = ' %s %s is Interested in you.' % (user_sender.first_name, user_sender.last_name)
        # mail_data['message'] = '''
        #     %s %s, <br> %s %s is Interested in talking to you. To answer check your inbox.<br>
        #                 <h3>People: %s</h3>
        #                 <br>
        #                 <h3>Sessions: %s</h3>
        #                 <br>
        #                 <h3>Details: </h3><br>
        #                 %s
        #                        ''' % (user_receiver.first_name, user_receiver.last_name, user_sender.first_name, user_sender.last_name, content)
        # mail_data['from'] = 'training@fyt.com'
        # mail_data['sender'] = user_sender.email
        # mail_data['receiver'] = user_receiver.email
        # send_mail(mail_data)
            return redirect('trainer', id=user_receiver.id)
            # return HttpResponse([{'code': 1, 'status': 'success'}])
        except Exception:
            return HttpResponse([{'code': -1, 'status': 'error', 'info': 'invalid_request'}])
    else:
        return HttpResponse([{'code': -1, 'status': 'error', 'info': 'invalid_data'}])


@requires_post
@json_response
def send_message(request):
    form = message_form(request.POST)
    if form.is_valid():
        # try:
        user_sender = User.objects.get(pk=request.POST.get('sender'))
        user_receiver = User.objects.get(pk=request.POST.get('receiver'))
        content = form.cleaned_data['message']
        conversation = Conversation.objects.get(id=request.POST.get('conversation'))
        Message.objects.create(conversation=conversation, sender=user_sender, receiver=user_receiver, message=content)
        # mail_data = {}
        # mail_data['subject'] = ' %s %s is Interested in you.' % (user_sender.first_name, user_sender.last_name)
        # mail_data['message'] = '''
        #     %s %s, <br> %s %s is Interested in talking to you. To answer check your inbox.<br>
        #                 <h3>People: %s</h3>
        #                 <br>
        #                 <h3>Sessions: %s</h3>
        #                 <br>
        #                 <h3>Details: </h3><br>
        #                 %s
        #                        ''' % (user_receiver.first_name, user_receiver.last_name, user_sender.first_name, user_sender.last_name, content)
        # mail_data['from'] = 'training@fyt.com'
        # mail_data['sender'] = user_sender.email
        # mail_data['receiver'] = user_receiver.email
        # send_mail(mail_data)
        # import ipdb; ipdb.set_trace()
        return redirect('dashboard_messages', conversation.id)
        # except Exception:
            # return [{'code': -1, 'status': 'error'}]
    else:
        return HttpResponse([{'code': -1, 'status': 'error', 'info': 'invalid_data'}])
