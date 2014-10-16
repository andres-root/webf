# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login

from forms import RegisterUserForm, BookForm, signinForm, ReviewForm, SignupForm
from models import TrainerProfile, UserProfile, Review
from messenger.models import Message
from authsys.models import User
import functions as utils


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/search')
    ctx = {}
    ctx['form'] = signinForm()
    return render_to_response('www/index.html', ctx, context_instance=RequestContext(request))


def search(request):
    trainers = User.objects.filter(is_trainer=True)
    ctx = {}
    ctx['trainers'] = trainers
    return render_to_response('www/search.html', ctx, context_instance=RequestContext(request))


def signup3(request):
    return render_to_response('web/signup.html', context_instance=RequestContext(request))


def signup2(request):
    return render_to_response('web/signup2.html', context_instance=RequestContext(request))


def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/search')

    if request.method == 'POST':
        form = SignupForm(request.POST or None)
        # form = RegisterUserForm(request.POST)
        if request.POST.get('is_trainer', ''):
            is_trainer = True
        else:
            is_trainer = False
        if form.is_valid():
            user = User.objects.create_user(email=request.POST.get('email', ''), username=request.POST.get('username', ''), password=request.POST.get('password', ''), first_name=request.POST.get('first_name', ''), last_name=request.POST.get('last_name', ''), is_trainer=is_trainer)
            if user.is_active:
                user_auth = authenticate(username=request.POST.get('username', ''), password=request.POST.get('password', ''))
                if user_auth is not None:
                    login(request, user_auth)
                    if is_trainer:
                        return HttpResponseRedirect('/signup/step-2')
                    else:
                        return HttpResponseRedirect('/search/')
                else:
                    return HttpResponseRedirect('/')

            #return HttpResponseRedirect('/continue/')
            else:
                return HttpResponseRedirect('/')
    # form = userCreationForm()
    ctx = {}
    form = SignupForm()
    ctx['form'] = form
    return render_to_response('web/signup3.html', ctx, context_instance=RequestContext(request))


def signin(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/search')
    else:
        if request.method == 'POST':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.POST.get('user_type', '') == '2':
                    return HttpResponseRedirect('/signup/step-2')
                else:
                    return HttpResponseRedirect('/search')
            else:
                return HttpResponseRedirect('/')
        else:
            ctx = {}
            ctx['form'] = signinForm()
            return render_to_response('web/signin.html', ctx, context_instance=RequestContext(request))


def continueReg(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/search')
    else:
        if request.method == 'POST':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/signup/step-2')
            else:
                return HttpResponseRedirect('/continue/')
        else:
            ctx = {}
            ctx['form'] = signinForm()
            return render_to_response('web/signin.html', ctx, context_instance=RequestContext(request))


def signout(request):
    logout(request)
    return HttpResponseRedirect('/')


def trainer(request, id):
    trainer = User.objects.get(id=id)
    reviews = Review.objects.filter(id_receiver=id)
    ctx = {}
    book_form = BookForm()
    review_form = ReviewForm()
    ctx['bookForm'] = book_form
    ctx['reviewForm'] = review_form
    ctx['trainer'] = trainer
    ctx['reviews'] = reviews
    #return render_to_response('web/trainer.html', ctx, context_instance=RequestContext(request))
    return render_to_response('profile/trainer_profile.html', ctx, context_instance=RequestContext(request))


def book(request):
    saved = False
    people =  0
    sessions = 0
    message = ''
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            user_sender = User.objects.get(pk=request.POST['id_sender'])
            user_receiver = User.objects.get(pk=request.POST['id_receiver'])
            sent = True
            people = form.cleaned_data['people']
            sessions = form.cleaned_data['sessions']
            message = form.cleaned_data['message']
            bm = Message()
            bm.id_sender = user_sender
            bm.id_receiver = user_receiver
            bm.message = message
            bm.people = people
            bm.sessions = sessions
            bm.save()
            mail_data = {}
            mail_data['subject'] = ' %s %s is Interested in you.' % (user_sender.first_name, user_sender.last_name)
            mail_data['message'] = '''
                %s %s, <br> %s %s is Interested in talking to you. To answer check your inbox.<br>
                            <h3>People: %s</h3>
                            <br>
                            <h3>Sessions: %s</h3>
                            <br>
                            <h3>Details: </h3><br>
                            %s
                                   ''' % (user_receiver.first_name, user_receiver.last_name, user_sender.first_name, user_sender.last_name, people, sessions, message)
            mail_data['from'] = 'training@fyt.com'
            mail_data['sender'] = user_sender.email
            mail_data['receiver'] = user_receiver.email
            sent = utils.send_mail(mail_data)
            saved = True
            return HttpResponseRedirect('/search/')
        else:
            return HttpResponseRedirect('/')


def respond(request):
    saved = False
    people =  0
    sessions = 0
    message = ''
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            user_sender = User.objects.get(pk=request.POST['id_sender'])
            user_receiver = User.objects.get(pk=request.POST['id_receiver'])
            sent = True
            people = form.cleaned_data['people']
            sessions = form.cleaned_data['sessions']
            message = form.cleaned_data['message']
            bm = Message()
            bm.id_sender = user_sender
            bm.id_receiver = user_receiver
            bm.message = message
            bm.people = people
            bm.sessions = sessions
            bm.save()
            mail_data = {}
            mail_data['subject'] = ' %s %s is Interested in you.' % (user_sender.first_name, user_sender.last_name)
            mail_data['message'] = '''
                %s %s, <br> %s %s is Interested in talking to you. To answer check your inbox.<br>
                            <h3>People: %s</h3>
                            <br>
                            <h3>Sessions: %s</h3>
                            <br>
                            <h3>Details: </h3><br>
                            %s
                                   ''' % (user_receiver.first_name, user_receiver.last_name, user_sender.first_name, user_sender.last_name, people, sessions, message)
            mail_data['from'] = 'training@fyt.com'
            mail_data['sender'] = user_sender.email
            mail_data['receiver'] = user_receiver.email
            sent = utils.send_mail(mail_data)
            saved = True
            return HttpResponseRedirect('/search/')
        else:
            return HttpResponseRedirect('/')


def review(request):
    saved = False
    review = ''
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            user_sender = User.objects.get(pk=request.POST['id_sender'])
            user_receiver = User.objects.get(pk=request.POST['id_receiver'])
            content = request.POST['content']
            sent = True
            re = Review()
            re.id_sender = user_sender
            re.id_receiver = user_receiver
            re.content = content
            re.save()
            mail_data = {}
            mail_data['subject'] = 'You have a new review.'
            mail_data['message'] = '''
                %s %s, <br> %s %s wrote a review about you. Here are the details<br>
                            <h3>Details: </h3><br>
                            %s
                                   ''' % (user_receiver.first_name, user_receiver.last_name, user_sender.first_name, user_sender.last_name, content)
            mail_data['from'] = 'training@fyt.com'
            mail_data['sender'] = user_sender.email
            mail_data['receiver'] = user_receiver.email
            sent = utils.send_mail(mail_data)
            saved = True
            return HttpResponseRedirect('/trainer/%d' % (user_receiver.id))
        else:
            return HttpResponseRedirect('/')


def profile(request, id):
    ctx = {}
    profile = UserProfile.objects.filter(user=id)
    trainer = TrainerProfile.objects.filter(user=id)
    messages = Message.objects.filter(id_receiver=id)
    first_message = Message.objects.filter(id_receiver=id)[:1].get()
    ctx['profile'] = profile
    ctx['trainer'] = trainer
    ctx['messages'] = messages
    ctx['first_message'] = first_message
    return render_to_response('web/profile.html', ctx, context_instance=RequestContext(request))


def messages(request):
    user = request.user
    ctx = {}
    profile = UserProfile.objects.filter(user=user.id)
    trainer = TrainerProfile.objects.filter(user=user.id)
    messages = Message.objects.filter(id_receiver=user.id)
    first_message = Message.objects.filter(id_receiver=user.id)[:1].get()
    ctx['profile'] = profile
    ctx['trainer'] = trainer
    ctx['messages'] = messages
    ctx['first_message'] = first_message
    return render_to_response('web/messages.html', ctx, context_instance=RequestContext(request))


def profileCalendar(request):
    ctx = {}
    return render_to_response('web/profile-calendar.html', ctx, context_instance=RequestContext(request))


def profileInfo(request):
    ctx = {}
    return render_to_response('web/profile-info.html', ctx, context_instance=RequestContext(request))
