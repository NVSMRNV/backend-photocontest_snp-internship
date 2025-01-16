from rest_framework import serializers

from config.settings.config import BASE_DOMAIN
from models.models.posts.models import Post


class RetrievePostSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, instance):
        return ''.join(BASE_DOMAIN + instance.image.url)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'description', 'image', 'created']
