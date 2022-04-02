# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.shortcuts import render
from utility.models import Project, Publication
from utility.views import contact_us_list
from freezer_inventory.views import freezer_inventory_return_metadata_table


class IndexTemplateView(TemplateView):
    # public template, to make private add LoginRequiredMixin
    # https://www.paulox.net/2020/12/08/maps-with-django-part-1-geodjango-spatialite-and-leaflet/
    # https://leafletjs.com/examples/geojson/
    template_name = 'home/django-material-kit/index.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'index'
        return context


@login_required(redirect_field_name='next', login_url="/login/")
def main_pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/django-material-kit/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/django-material-kit/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/django-material-kit/page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(redirect_field_name='next', login_url="/dashboard/login/")
def dashboard_index(request):
    return_metadata_table, return_metadata_count = freezer_inventory_return_metadata_table(request)
    contactus_list, replied_count = contact_us_list(request)
    context = {'segment': 'index',
               'return_metadata_table': return_metadata_table,
               'return_metadata_count': return_metadata_count,
               'contactus_list': contactus_list,
               'replied_count': replied_count}

    html_template = loader.get_template('home/django-material-dashboard/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(redirect_field_name='next', login_url="/dashboard/login/")
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

        html_template = loader.get_template('home/django-material-kit/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/django-material-kit/page-500.html')
        return HttpResponse(html_template.render(context, request))
