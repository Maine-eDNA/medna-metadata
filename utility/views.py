from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProcessLocationSerializer, GrantProjectSerializer
from .models import ProcessLocation, GrantProject


# Create your views here.
class GrantProjectViewSet(viewsets.ModelViewSet):
    serializer_class = GrantProjectSerializer
    queryset = GrantProject.objects.all()


class ProcessLocationViewSet(viewsets.ModelViewSet):
    serializer_class = ProcessLocationSerializer
    queryset = ProcessLocation.objects.all()
