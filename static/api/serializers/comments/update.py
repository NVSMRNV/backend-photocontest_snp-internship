from rest_framework import serializers

from models.models.comments.models import Comment


class UpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text',]
        extra_kwargs = {
            'text': {'required': False},
        } 