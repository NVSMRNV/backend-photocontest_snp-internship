from rest_framework import serializers

from models.models.votes.models import Vote


class CreateVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
