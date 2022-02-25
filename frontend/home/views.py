# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from utility.models import Project, Publication


@login_required(login_url="/login/")
def main_index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/django-material-kit/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def main_pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        if load_template == 'projects.html':
            project_list = Project.objects.prefetch_related('created_by', 'grant_names').order_by('pk')
            context = {'project_list': project_list}
            return render(request, 'home/django-material-kit/projects.html', context)

        if load_template == 'publications.html':
            pub_list = Publication.objects.prefetch_related('created_by', 'project_names', 'publication_authors').order_by('pk')
            context = {'pub_list': pub_list}
            return render(request, 'home/django-material-kit/publications.html', context)

        html_template = loader.get_template('home/django-material-kit/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/django-material-kit/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/django-material-kit/page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/dashboard/login/")
def dashboard_index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/django-material-dashboard/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/dashboard/login/")
def dashboard_pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/django-material-dashboard/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/django-material-dashboard/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/django-material-dashboard/page-500.html')
        return HttpResponse(html_template.render(context, request))
