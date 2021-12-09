from rest_framework import viewsets
from .serializers import CustomUserSerializer
from .models import CustomUser


# Create your views here.
class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    filterset_fields = ['email', 'agol_username', 'is_staff', 'is_active', 'expiration_date']
