from uuid import uuid1
from rest_framework import serializers
from Devices.models import (
    Device,
    Sensor,
    PinOfDevice,
    SensorForDevice,
    TimeEnable,
    RelayForDevice,
    Relay,
    SensorValueType,
)

class DeviceSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    versions = serializers.IntegerField()
    release = serializers.FileField( allow_null=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = Device
        fields = ('pk','name','versions','release','user')
    


class SensoreSerializer(serializers.ModelSerializer):
    uniq_name = serializers.CharField()
    class Meta:
        model = Sensor
        fields = ('pk','uniq_name','pin_number')



class RelaySerializer(serializers.ModelSerializer):
    uniq_name = serializers.CharField()
    class Meta:
        model = Relay
        fields = ('pk','uniq_name',)

class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = PinOfDevice
        fields = ('pk','device','pin_number','pin')


class SensorForDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorForDevice
        fields = ('pk','device','sensor','enable',)

class RelayForDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelayForDevice
        fields = ('pk','device','relay','enable',)

class SensorValueTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorValueType
        fields = ('pk','sensor','sort','name','types')


class TimeEnableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeEnable
        fields = ('pk','sensorfordevice','start_day','end_day','start_time','end_time')