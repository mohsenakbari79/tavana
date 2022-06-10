from uuid import uuid1
from rest_framework import serializers


class DeviceSerializer(serializers.Serializer):
    name = serializers.CharField()
    versions = serializers.IntegerField()
    release = serializers.FileField()

class SensoreSerializer(serializers.Serializer):
     uniq_name = serializers.CharField()


