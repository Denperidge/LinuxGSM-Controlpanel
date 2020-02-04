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
    
    return render(request, 'index.html')

@login_required
def lgsm(request):
    if request.user.is_staff:
        return HttpResponseRedirect('/admin/')
    
    output = lgsmCommand(request.user, request.GET["command"])

    # Return JSON, has to be in double quotes to work
    output = output.replace('"', '\\"').replace("'", '"')

    return HttpResponse(output)

