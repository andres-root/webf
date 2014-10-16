# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from authsys.factory import UserFactory


class MessengerTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create()
        self.user_sender = UserFactory.create()
        self.user_receiver = UserFactory.create()
        self.user_sender.email = 'strike1609@gmail.com'
        self.user_receiver.email = 'andres.root.coder@gmail.com'
        self.client.login(username=self.user.username,
                          password=UserFactory.DEFAULT_PASSWORD)

    def test_create_conversation(self):
        # try:
        response = self.client.post(reverse('create_conversation'), {'sender': self.user_sender.id, 'receiver': self.user_receiver.id, 'message': 'This is a Test!'}).content
        print response
        # except Exception:
            # print 'failed!'

    # def test_send_message(self):
        # try:
            # response = self.client.post(reverse('send_message'), {}).content
            # print response
        # except Exception:
            # print 'failed!'
