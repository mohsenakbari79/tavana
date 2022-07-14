from uuid import uuid1
from rest_framework import serializers
from Devices.models import Device,Sensor,PinOfDevice,SensorForDevice

class DeviceSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    versions = serializers.IntegerField()
    release = serializers.FileField( allow_null=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = Device
        fields = ('name','versions','release','user')


class SensoreSerializer(serializers.ModelSerializer):
    uniq_name = serializers.CharField()
    class Meta:
        model = Sensor
        fields = ('uniq_name','pin_number')

class RelaySerializer(serializers.ModelSerializer):
    uniq_name = serializers.CharField()
    class Meta:
        model = Sensor
        fields = ('uniq_name',)

class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = PinOfDevice
        fields = ('device','pin_number','pin')


class SensorForDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorForDevice
        fields = ('device','sensor','enable',)

class RelayForDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorForDevice
        fields = ('device','sensor','enable',)

class TimeEnableSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorForDevice
        fields = ('sensorfordevice','start_day','end_day','start_time','end_time')