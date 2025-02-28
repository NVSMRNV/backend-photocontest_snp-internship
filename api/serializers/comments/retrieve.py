from rest_framework import serializers

from models.models.comments.models import Comment


class RetrieveCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        