# -*- encoding: utf-8 -*-
# Copyright (c) 2019 - present AppSeed.us
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm


# Create your views here.
def main_login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == 'POST':

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, 'account/django-material-kit/login.html', {'form': form, 'msg': msg})


def dashboard_login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == 'POST':

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/dashboard/')
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, 'account/django-material-dashboard/login.html', {'form': form, 'msg': msg})


def main_register_user(request):
    msg = None
    success = False

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect('/login/')

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, 'account/django-material-kit/register.html', {'form': form, 'msg': msg, 'success': success})


def dashboard_register_user(request):
    msg = None
    success = False

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/dashboard/login">login</a>.'
            success = True

            # return redirect('/dashboard/login/')

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, 'account/django-material-dashboard/register.html', {'form': form, 'msg': msg, 'success': success})
