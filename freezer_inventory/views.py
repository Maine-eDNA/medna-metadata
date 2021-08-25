from django.shortcuts import render
from .serializers import FreezerSerializer, FreezerRackSerializer, FreezerBoxSerializer, FreezerInventorySerializer, \
    FreezerCheckoutSerializer
from .models import Freezer, FreezerRack, FreezerBox, FreezerInventory, FreezerCheckout
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
# Create your views here.


class FreezerViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerSerializer
    queryset = Freezer.objects.all()
    filterset_fields = ['created_by']
    filter_backends = [DjangoFilterBackend]


class FreezerRackViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerRackSerializer
    queryset = FreezerRack.objects.all()
    filterset_fields = ['freezer', 'created_by']
    filter_backends = [DjangoFilterBackend]


class FreezerBoxViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerBoxSerializer
    queryset = FreezerBox.objects.all()
    filterset_fields = ['freezer_rack', 'created_by']
    filter_backends = [DjangoFilterBackend]


class FreezerInventoryViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerInventorySerializer
    queryset = FreezerInventory.objects.all()
    filterset_fields = ['freezer_box', 'field_sample', 'extraction', 'created_by']
    filter_backends = [DjangoFilterBackend]


class FreezerCheckoutViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerCheckoutSerializer
    queryset = FreezerCheckout.objects.all()
    filterset_fields = ['freezer_inventory', 'created_by']
    filter_backends = [DjangoFilterBackend]
