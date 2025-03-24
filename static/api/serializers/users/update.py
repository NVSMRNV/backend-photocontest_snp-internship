from rest_framework import serializers

from models.models.users.models import User


class UpdateUserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ['username', 'email', 'profile_photo', 'bio']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'bio': {'required': False},
        }       
