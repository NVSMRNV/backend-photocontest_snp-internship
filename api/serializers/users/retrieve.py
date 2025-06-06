from rest_framework import serializers

from config.settings.config import BASE_DOMAIN
from models.models.users.models import User


class RetrieveUserSerializer(serializers.ModelSerializer):
    profile_photo = serializers.SerializerMethodField()

    def get_profile_photo(self, instance):
        return BASE_DOMAIN + instance.profile_photo.url if instance.profile_photo else None
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_photo', 'bio']
