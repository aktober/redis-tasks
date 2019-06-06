from rest_framework import serializers


class TaskSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=256)
