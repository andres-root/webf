# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from authsys.models import User
from authsys.forms import signin_form


def signin(request):
    """
    SignInView
    """
    if request.user.is_authenticated():
        return redirect('/search')
    else:
        if request.method == 'POST':
            form = signin_form(request.POST or None)
            if form.is_valid():
                email = request.POST.get('email', '')
                password = request.POST.get('password', '')
                try:
                    user = User.objects.get(email=email)
                except:
                    return redirect('/')
                if user.is_active:
                    user_auth = authenticate(username=email, password=password)
                    if user_auth is not None:
                        login(request, user_auth)
                        if request.POST.get('user_type', '') == '2':
                            return redirect('/signup/step-2')
                        else:
                            return redirect('/search')
                    else:
                        return redirect('/')
            else:
                return redirect('/')
        else:
            ctx = {}
            ctx['form'] = signin_form()
            return render(request, 'web/signin.html', ctx)


def signout(request):
    """
    Cierra la session del usuario
    """
    logout(request)
    return redirect('/')
