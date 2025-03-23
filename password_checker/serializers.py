from rest_framework import serializers

class PasswordCheckSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, write_only=True)