from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from Devices.models import Device,Sensor,PinOfDevice,SensorForDevice
from Devices.serializers import DeviceSerializer,SensoreSerializer,PinSerializer,SensoreForDeviceSerializer
from collections import Counter,defaultdict
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status

import json
class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    http_method_names = ['post', 'get', 'delete', 'put']
    search_fields = ('hostname',)
    
   

class SensorViewSet(ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class =  SensoreSerializer
    http_method_names = ['post', 'get', 'delete', 'put']
    search_fields = ('uniq_name')

class SensorForDeviceViewSet(ModelViewSet):
    queryset = SensorForDevice.objects.all()
    serializer_class =  SensoreForDeviceSerializer
    http_method_names = ['post' , 'get', 'delete', 'put']
    search_fields = ('uniq_name')

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset

    def list(self, request, *args, **kwargs):
        result = super().list(request, *args, **kwargs)
        return result


    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):

        return super().update(request, *args, **kwargs)

class PinForDeviceViewSet(ModelViewSet):
    queryset = PinOfDevice.objects.all()
    serializer_class = PinSerializer
    http_method_names = ['post', 'get', 'delete', 'put']   

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset

    def list(self, request, *args, **kwargs):
        result = super().list(request, *args, **kwargs)
        return result


    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        pin = json.loads(request.data.get("pin"))
        if pin != None:
            pin_counter=dict(Counter(pin.values()))
            pin_counter.pop(None)
            try:
                for key,value in pin_counter.items():
                    sensor = self.queryset.get(pk=kwargs["pk"]).device.device_sensor.get(pk=key).sensor
                    if value != sensor.pin_number :
                        return Response({'error': f"A sensor {sensor.uniq_name} has {sensor.pin_number} pins while you have given {sensor}"}, status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                return Response({'error': f"Use the corresponding device sensors for all pins"}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs) 

