from rest_framework import serializers


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=127)
    password = serializers.CharField(max_length=127)
