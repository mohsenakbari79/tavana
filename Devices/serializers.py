from uuid import uuid1
from rest_framework import serializers
from Devices.models import Device,Sensor,PinOfDevice,SensorForDevice

class DeviceSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    versions = serializers.IntegerField()
    release = serializers.FileField( allow_null=True)
    class Meta:
        model = Device
        fields = ('name','versions','release')


class SensoreSerializer(serializers.ModelSerializer):
    uniq_name = serializers.CharField()
    class Meta:
        model = Sensor
        fields = ('uniq_name','pin_number')


class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = PinOfDevice
        fields = ('device','pin_number','pin')


class SensoreForDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorForDevice
        fields = ('device','sensor','enable',)