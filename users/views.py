from rest_framework import viewsets
from .serializers import CustomUserSerializer
from .models import CustomUser

# Create your views here.

class CustomUserView(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()