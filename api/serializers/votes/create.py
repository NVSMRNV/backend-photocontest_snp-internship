from rest_framework import serializers

from api.serializers.users.retrieve import RetrieveUserSerializer
from models.models.votes.models import Vote


class CreateVoteSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    post_id = serializers.IntegerField()
