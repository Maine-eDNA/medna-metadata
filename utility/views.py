from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProcessLocationSerializer
from .models import ProcessLocation


# Create your views here.
class ProcessLocationViewSet(viewsets.ModelViewSet):
    serializer_class = ProcessLocationSerializer
    queryset = ProcessLocation.objects.all()
