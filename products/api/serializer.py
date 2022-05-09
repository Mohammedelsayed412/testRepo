from rest_framework import serializers
from products.models import AuditLog
from django.contrib.auth.models import User

class LogSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    userName = serializers.CharField(max_length=100)
    date = serializers.DateTimeField(read_only=True, format=None,input_formats=None)
    ip = serializers.IPAddressField()
    eventName = serializers.CharField(max_length=100)
    description =  serializers.CharField(max_length=500)
    actionType = serializers.CharField(max_length=100)
    eventSpecificFields =  serializers.JSONField()

    def create(self, validated_data):
        return AuditLog.objects.create(**validated_data)

