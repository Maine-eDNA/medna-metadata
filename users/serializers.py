from rest_framework import serializers

from users.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['pk', 'email', 'first_name', 'last_name', 'phone_number']
        read_only_fields = ('email',)