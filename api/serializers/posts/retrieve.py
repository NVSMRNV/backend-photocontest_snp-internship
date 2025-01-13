from rest_framework import serializers

from models.models.posts.models import Post


class RetrievePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'description', 'image', ]
