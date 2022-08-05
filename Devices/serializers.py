from uuid import uuid1
from rest_framework import serializers
from Devices.models import (
    Device,
    Sensor,
    PinOfDevice,
    SensorForDevice,
    # TimeEnable,
    RelayForDevice,
    Relay,
    SensorValueType,
    Operators,
    SensorDeviceValidation,
    # TimeAction,
    DeviceModels,

)
from django_celery_beat.models import CrontabSchedule,PeriodicTask
from timezone_field.rest_framework import TimeZoneSerializerField

class DeviceModelsSerializer(serializers.ModelSerializer):
    versions = serializers.IntegerField()
    release = serializers.FileField()
    class Meta:
        model = DeviceModels
        fields = ("pk","name","versions","release",)
    


class DeviceSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = Device
        fields = ('pk','name','deviceModel','user')
    


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
    def get_device(self,obj):
        return {
            "pk":obj.device.pk,
            "name":obj.device.name,
            "model":obj.device.deviceModel.name
                }
    device=serializers.SerializerMethodField("get_device")
    
    class Meta:
        model = PinOfDevice
        fields = ('pk','device','pin_number','pin')
        read_only_fields = ["device"]

class FilterDeviceWithUser(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        return Device.objects.filter(user=user)


class SensorForDeviceSerializer(serializers.ModelSerializer):
    device = FilterDeviceWithUser()
    class Meta:
        model = SensorForDevice
        fields = ('pk','device','sensor','enable',)

class RelayForDeviceSerializer(serializers.ModelSerializer):
    device = FilterDeviceWithUser()
    class Meta:
        model = RelayForDevice
        fields = ('pk','device','relay','enable',)

class SensorValueTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorValueType
        fields = ('pk','sensor','sort','name','types')



class OperatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operators
        fields = ('pk','operator_type','operaror_name')


class SensorDeviceValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorDeviceValidation
        fields = ('pk',"device_sensor","sort","senortype","relay","operator","operator_value","active")


class CrontabScheduleSerializer(serializers.ModelSerializer):
    timezone=TimeZoneSerializerField(use_pytz=False)
    class Meta:
        model = CrontabSchedule
        fields = "__all__"

class PeriodicTaskSerializer(serializers.ModelSerializer):
    crontab = CrontabScheduleSerializer()
    class Meta:
        model = PeriodicTask
        fields = ("name","crontab","task","args","enabled","one_off")
    def create(self, validated_data):
        Crontab = CrontabSchedule.objects.create(**validated_data.pop('crontab'))
        instance=PeriodicTask.objects.create(**validated_data,crontab=Crontab)
        return instance

class FilterRelayForeignKeyWithUser(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        return RelayForDevice.objects.filter(device__user=user)







