from django.shortcuts import render
from .serializers import FreezerSerializer, FreezerRackSerializer, FreezerBoxSerializer, FreezerInventorySerializer, \
    FreezerCheckoutSerializer
from .models import Freezer, FreezerRack, FreezerBox, FreezerInventory, FreezerCheckout
from utility.serializers import MultipleFieldLookupMixin
from rest_framework import viewsets
# Create your views here.


class FreezerViewSet(viewsets.ModelViewSet, MultipleFieldLookupMixin):
    serializer_class = FreezerSerializer
    queryset = Freezer.objects.all()
    lookup_fields = ['created_by']


class FreezerRackViewSet(viewsets.ModelViewSet, MultipleFieldLookupMixin):
    serializer_class = FreezerRackSerializer
    queryset = FreezerRack.objects.all()
    lookup_fields = ['freezer', 'created_by']


class FreezerBoxViewSet(viewsets.ModelViewSet, MultipleFieldLookupMixin):
    serializer_class = FreezerBoxSerializer
    queryset = FreezerBox.objects.all()
    lookup_fields = ['freezer_rack', 'created_by']


class FreezerInventoryViewSet(viewsets.ModelViewSet, MultipleFieldLookupMixin):
    serializer_class = FreezerInventorySerializer
    queryset = FreezerInventory.objects.all()
    lookup_fields = ['freezer_box', 'field_sample', 'extraction', 'created_by']


class FreezerCheckoutViewSet(viewsets.ModelViewSet, MultipleFieldLookupMixin):
    serializer_class = FreezerCheckoutSerializer
    queryset = FreezerCheckout.objects.all()
    lookup_fields = ['freezer_inventory', 'created_by']
