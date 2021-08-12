from django.shortcuts import render
from .serializers import FreezerSerializer, FreezerRackSerializer, FreezerBoxSerializer, FreezerInventorySerializer, \
    FreezerCheckoutSerializer
from .models import Freezer, FreezerRack, FreezerBox, FreezerInventory, FreezerCheckout
from rest_framework import viewsets
# Create your views here.


class FreezerViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerSerializer
    queryset = Freezer.objects.all()


class FreezerRackViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerRackSerializer
    queryset = FreezerRack.objects.all()


class FreezerBoxViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerBoxSerializer
    queryset = FreezerBox.objects.all()


class FreezerInventoryViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerInventorySerializer
    queryset = FreezerInventory.objects.all()


class FreezerCheckoutViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerCheckoutSerializer
    queryset = FreezerCheckout.objects.all()
