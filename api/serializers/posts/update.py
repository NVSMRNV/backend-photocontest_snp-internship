from rest_framework import serializers

from models.models.posts.models import Post


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image',]
        extra_kwargs = {
            'title': {'required': False},
            'description': {'required': False},
            'image': {'required': False},
        } 