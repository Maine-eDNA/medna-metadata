from rest_framework import viewsets
from .serializers import CustomUserSerializer, CustomLoginSerializer
from .models import CustomUser

# Create your views here.

class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class CustomUserLoginViewSet(viewsets.ModelViewSet):
    serializer_class = CustomLoginSerializer
    queryset = CustomUser.objects.all()
