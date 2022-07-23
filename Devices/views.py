from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import authentication, permissions
from Devices.amqp import PMI
from Auth.models import User
from Devices.models import (
    Device,
    Sensor,
    Relay,
    PinOfDevice,
    SensorForDevice,
    RelayForDevice,
    TimeEnable,
    SensorValueType,
    Operators,
    SensorDeviceValidation,
)
from Devices.serializers import (
    DeviceSerializer,
    SensoreSerializer,
    PinSerializer,
    SensorForDeviceSerializer,
    RelayForDeviceSerializer,
    RelaySerializer,
    TimeEnableSerializer,
    SensorValueTypeSerializer,
    SensorDeviceValidationSerializer,
    OperatorsSerializer,

)
from collections import Counter,defaultdict
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from Devices.utils import redisclient,pin_and_sensor_of_device,ralay_for_device_update
import json
import asyncio

class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    http_method_names = ['post', 'get', 'delete', 'put']
    search_fields = ('hostname',)
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        queryset = queryset.filter(user=self.request.user)
        return queryset
    def create(self, request, *args, **kwargs):
        if self.queryset.filter(name=request.POST.get("name")).exists():
            return Response({'error': f"name is uniq please not enter anouter name"}, status=status.HTTP_400_BAD_REQUEST)
        device=super().create(request, *args, **kwargs)
        PinOfDevice(device=self.queryset.get(name=device.data.get("name"))).save()
        return device
    

class OperatorsViewSet(ModelViewSet):
    queryset = Operators.objects.all()
    serializer_class =  OperatorsSerializer
    http_method_names = ['post' , 'get', 'delete', 'put']

    
class SensorDeviceValidationViewSet(ModelViewSet):
    queryset = SensorDeviceValidation.objects.all()
    serializer_class =  SensorDeviceValidationSerializer
    http_method_names = ['post' , 'get', 'delete', 'put']


class SensorViewSet(ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class =  SensoreSerializer
    http_method_names = ['post', 'get', 'delete', 'put']
    search_fields = ('uniq_name',)

class RelayViewSet(ModelViewSet):
    queryset = Relay.objects.all()
    serializer_class =  RelaySerializer
    http_method_names = ['post' , 'get', 'delete', 'put']
    search_fields = ('uniq_name',)

class RelayForDeviceViewSet(ModelViewSet):
    queryset = RelayForDevice.objects.all()
    serializer_class =  RelayForDeviceSerializer
    http_method_names = ['post' , 'get', 'delete', 'put']
    search_fields = ('uniq_name',)
    def update(self, request, *args, **kwargs):
        result=  super().update(request, *args, **kwargs)
        relay=self.queryset.get(pk=kwargs["pk"]).device
        answer =ralay_for_device_update(relay,device)
        if answer[0] == True:
            PMI.send_message(device.auth.mac_addres,answer[1])
        return result
class SensorValueTypeViewSet(ModelViewSet):
    queryset = SensorValueType.objects.all()
    serializer_class = SensorValueTypeSerializer
    http_method_names = ['post' , 'get', 'delete', 'put']
    search_fields = ('name',)

class SensorForDeviceViewSet(ModelViewSet):
    queryset = SensorForDevice.objects.all()
    serializer_class =  SensorForDeviceSerializer
    http_method_names = ['post' , 'get', 'delete', 'put']
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

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
        result=  super().update(request, *args, **kwargs)
        device=self.queryset.get(pk=kwargs["pk"]).device
        PMI.send_message(device.auth.mac_addres,pin_and_sensor_of_device(device))
        return result
class PinForDeviceViewSet(ModelViewSet):
    queryset = PinOfDevice.objects.all()
    serializer_class = PinSerializer
    http_method_names = ['get', 'delete', 'put']   

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
        try:
            pin = json.loads(request.data.get("pin"))
            device=self.queryset.get(pk=kwargs["pk"]).device
            if pin != None:
                pin_counter=dict(Counter(pin.values()))
                pin_counter.pop(None)
                for key,value in pin_counter.items():
                    key=str(key)
                    split_key=key.split("_")
                    sensor =None
                    if split_key[0] not in ["sensor","relay"]:
                        return Response({'error': f"A sensor {key} not good format (sensor_pk | relay_pk) "}, status=status.HTTP_400_BAD_REQUEST)
                    if split_key[0]=="sensor":
                        sensor = device.device_sensor.get(pk=split_key[1]).sensor
                    else:
                        relay = device.device_relay.get(pk=split_key[1]).relay
                    if sensor != None and value != sensor.pin_number :
                        return Response({'error': f"A sensor {sensor.uniq_name} has {sensor.pin_number} pins while you have given {sensor}"}, status=status.HTTP_400_BAD_REQUEST)
                    elif value != 1:
                        return Response({'error': f"A relay can just one pins"}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'error': f"Use the corresponding device sensors for all pins"}, status=status.HTTP_400_BAD_REQUEST)
        PinFdevice = super().update(request, *args, **kwargs)
        device=self.queryset.get(pk=kwargs["pk"]).device
        if device.auth.mac_addres is not None:
            PMI.send_message(device.auth.mac_addres,pin_and_sensor_of_device(device))
        return PinFdevice



class TimeDefualtValueViewSet(ModelViewSet):
    queryset = TimeEnable.objects.all()
    serializer_class =  TimeEnableSerializer
    http_method_names = ['post' , 'get', 'delete', 'put']
    # search_fields = ('uniq_name')

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        all_time=self.queryset.filter(sensorfordevice=kwargs["sensorfordevice"])
        if (kwargs["end_day"] != None and kwargs["start_day"] < kwargs["end_day"]) or (kwargs["end_time"] != None and kwargs["start_time"] < kwargs["end_time"]):
            pass
        for time_check in all_time:          
            if kwargs["start_day"] != None and kwargs["end_day"] != None and\
                    time_check.start_day != None and time_check.start_day != None and  \
                    (time_check.start_day < d2.start_day < time_check.end_day) or (time_check.start_day < d2.end_day < time_check.end_day) or (d2.start_day <= time_check.start_day and d2.end_day >= time_check.end_day):       
                if kwargs["start_time"] != None and kwargs["end_time"] != None and\
                    time_check.start_time != None and time_check.start_time != None and  \
                    (time_check.start_time < d2.start_time < time_check.end_time) or (time_check.start_time < d2.end_time < time_check.end_time) or (d2.start_time <= time_check.start_time and d2.end_time >= time_check.end_time):
                    raise ValidationError()  
        return super().update(request, *args, **kwargs)
    


# @api_view(['GET', 'POST'])
# def sensorvalue(request,device,sensore=None):
#     try:
#         obj_device = Device.objects.get(name=device)
        
        
#         senosr_list=[]
#         rs=redisclient.query(f"select * from {obj_device.name}")
#         respons ={"device":obj_device.name,"data":[]}
#         if sensore is not None:
#             senosr_list.append(list(rs.get_points(tags={"sensor_id": f"{sensore}"})))
#         else:
#             senosr=obj_device.device_sensor.all()
#             for sen in senosr:
#                 templist=list(rs.get_points(tags={"sensor_id": f"{sen.pk}"}))
#                 if 0<len(templist):
#                     senosr_list.extend(templist)
#         for value in senosr_list:
#             sensor=obj_device.device_sensor.get(sensor=value["sensor_id"]).sensor
#             respons["data"].append({
#                 "sensore":sensor.uniq_name,
#                 "value":value["data"],
#                 "time":value["time"],
#             })
#         return Response(data=respons)
#     except Exception as e:
#         print("salam",e, e.__traceback__.tb_lineno )
#         return Response({'error': f"not exit device or senore by id entered"}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'POST'])
def sensorvalue(request,device,sensore=None):
    try:
        obj_device = Device.objects.get(name=device)

        senosr_list=[]
        rs=redisclient.query(f"select * from {obj_device.name}")
        respons ={"device":obj_device.name,"data":[]}
        if sensore is not None:
            senosr_list.append(list(rs.get_points(tags={"sensor_id": f"{sensore}"})))
        else:
            senosr=obj_device.device_sensor.all()
            for sen in senosr:
                templist=list(rs.get_points(tags={"sensor_id": f"{sen.pk}"}))
                if 1==len(templist):
                    senosr_list.append(templist)
                elif 1<len(templist):
                    all_value={
                        "sensor_id":sen.pk,
                        "data":[value["data"] for value in templist],
                    }
                    senosr_list.append(all_value)
        for value in senosr_list:
            sensor=obj_device.device_sensor.get(sensor=value["sensor_id"]).sensor
            respons["data"].append({
                "sensore":sensor.uniq_name,
                "value":value["data"],
            })
        return Response(data=respons)
    except Exception as e:
        print("salam",e, e.__traceback__.tb_lineno )
        return Response({'error': f"not exit device or senore by id entered"}, status=status.HTTP_400_BAD_REQUEST)


