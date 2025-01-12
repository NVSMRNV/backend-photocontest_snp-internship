from rest_framework import serializers
from models.models.users.models import User


class RetrieveUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_photo', 'bio']

