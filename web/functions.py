# -*- coding: utf-8 -*-
from django.core.mail import EmailMultiAlternatives


def send_mail(data):
    subject = data['subject']
    content = data['message']
    from_mail = data['from']
    #sender = data['sender']
    receiver = data['receiver']

    msg = EmailMultiAlternatives(subject, content, from_mail, [receiver])
    msg.attach_alternative(content, 'text/html')
    msg.send()
    return msg
