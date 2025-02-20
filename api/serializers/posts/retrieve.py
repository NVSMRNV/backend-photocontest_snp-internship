from datetime import datetime

from rest_framework import serializers

from api.serializers.users.retrieve import RetrieveUserSerializer
from config.settings.config import BASE_DOMAIN
from models.models.posts.models import Post


class RetrievePostSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    author = RetrieveUserSerializer()
    created = serializers.SerializerMethodField()

    def get_created(self, instance):
        return instance.created.strftime("%d/%m/%Y • %H:%M")

    def get_image(self, instance):
        return ''.join(BASE_DOMAIN + instance.image.url)

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'title',
            'description',
            'image',
            'created',
            'votes_number',
            'comments_number',
        ]

