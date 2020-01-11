from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout

import json

from .daemon import lgsmCommand

def loginToGameserver(request):
    identifier = request.POST.get('username')
    password = request.POST.get('password')

    # If identifier or password isn't passed
    if not identifier or not password:
        user = None  # Don't attempt to authenticate/log in
    else:
        user = authenticate(request, username=identifier, password=password)
    
    if user is not None:
        login(request, user)
        # If it's an admin account, redirect to /admin/
        if user.is_staff:
            return HttpResponseRedirect('/admin/')
        return HttpResponseRedirect(request.POST.get('next'))

    else:
        return LoginView.as_view(
            template_name='admin/login.html',
            extra_context={
                'site_header': 'LGSM Controlpanel',
                'site_title': "Login",
                'title': "Lgsmcp",
                'app_path': '/login/'
            })(request)
  

def logoutOfGameserver(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def index(request):
    # If it's an admin account, redirect to /admin/
    if request.user.is_staff:
        return HttpResponseRedirect('/admin/')
    
    output = lgsmCommand(request.user, "start")

    # TODO Parse list
    # To parse list string, replace single quotes with double & do a json loads
    # If this method is used, improve replace to not replace *all* single quotes
    # output = json.loads(output)
    
    html = output
    
    return HttpResponse(html)

