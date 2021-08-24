from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProcessLocationSerializer, ProjectSerializer, GrantSerializer
from .models import ProcessLocation, Project, Grant
from django.views.generic.base import TemplateView



# Create your views here.
class GrantViewSet(viewsets.ModelViewSet):
    # formerly Project in field_sites.models
    serializer_class = GrantSerializer
    queryset = Grant.objects.all()


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class ProcessLocationViewSet(viewsets.ModelViewSet):
    serializer_class = ProcessLocationSerializer
    queryset = ProcessLocation.objects.all()


class IndexView(TemplateView):
    template_name = "utility/index.html"
