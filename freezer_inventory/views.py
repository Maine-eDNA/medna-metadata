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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']


class FreezerRackViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerRackSerializer
    queryset = FreezerRack.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['freezer', 'created_by']


class FreezerBoxViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerBoxSerializer
    queryset = FreezerBox.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['freezer_rack', 'created_by']


class FreezerInventoryViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerInventorySerializer
    queryset = FreezerInventory.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['freezer_box', 'freezer_inventory_type', 'freezer_inventory_status', 'created_by']


class FreezerCheckoutViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerCheckoutSerializer
    queryset = FreezerCheckout.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['freezer_inventory', 'freezer_checkout_action', 'created_by']
