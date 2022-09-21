from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from datetime import timedelta
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
    SensorValueType,
    Operators,
    SensorDeviceValidation,
    DeviceModels,
)
from Devices.serializers import (
    DeviceSerializer,
    SensoreSerializer,
    PinSerializer,
    SensorForDeviceSerializer,
    RelayForDeviceSerializer,
    RelaySerializer,
    SensorValueTypeSerializer,
    SensorDeviceValidationSerializer,
    OperatorsSerializer,
    DeviceModelsSerializer,
    PeriodicTaskSerializer,

)
from collections import Counter,defaultdict
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from Devices.utils import redisclient,pin_and_sensor_of_device,ralay_for_device_update
from rest_framework.permissions import IsAdminUser
from Devices.permissions import IsAdminUserOrGet
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from celery import current_app
from rest_framework.decorators import authentication_classes, permission_classes
import json
import asyncio
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class DeviceModelsViewSet(ModelViewSet):
    queryset = DeviceModels.objects.all()
    serializer_class = DeviceModelsSerializer
    http_method_names = ['post', 'get', 'delete', 'put']
    search_fields = ('hostname',)
    permission_classes =(IsAdminUserOrGet,)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset
    def create(self, request, *args, **kwargs):
        if self.queryset.filter(name=request.POST.get("name")).exists():
            return Response({'error': f"name is uniq please not enter anouter name"}, status=status.HTTP_400_BAD_REQUEST)
        device=super().create(request, *args, **kwargs)
        return device
    


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
    permission_classes =(IsAdminUserOrGet,)

    
class SensorDeviceValidationViewSet(ModelViewSet):
    queryset = SensorDeviceValidation.objects.all()
    serializer_class =  SensorDeviceValidationSerializer
    http_method_names = ['post' , 'get', 'delete', 'put']
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        queryset = queryset.filter(device_sensor__device__user=self.request.user)
        return queryset



class SensorViewSet(ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class =  SensoreSerializer
    http_method_names = ['post', 'get', 'delete', 'put']
    search_fields = ('uniq_name',)
    permission_classes =(IsAdminUserOrGet,)

class RelayViewSet(ModelViewSet):
    queryset = Relay.objects.all()
    serializer_class =  RelaySerializer
    http_method_names = ['post' , 'get', 'delete', 'put']
    search_fields = ('uniq_name',)
    permission_classes =(IsAdminUserOrGet,)

class RelayForDeviceViewSet(ModelViewSet):
    queryset = RelayForDevice.objects.all()
    serializer_class =  RelayForDeviceSerializer
    http_method_names = ['post' , 'get', 'delete', 'put']
    search_fields = ('uniq_name',)
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        queryset = queryset.filter(device__user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        result = super().create(request, *args, **kwargs)
        relay = self.queryset.get(pk=result.data["pk"])
        relay.enable = False
        relay.save()
        return result

    def destroy(self, request, *args, **kwargs):
        relay = RelayForDevice.objects.get(pk=kwargs["pk"])
        device_pin = relay.device.pinofdevice
        relay_id = "relay_" +str(relay.pk)
        if relay_id in device_pin.pin.values():
            for pin_pk, relay_pk in device_pin.pin.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
                if relay_pk == relay_id:
                    device_pin.pin[pin_pk]=None
            device_pin.save()
        return super().destroy(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        result=  super().update(request, *args, **kwargs)
        device=self.queryset.get(pk=kwargs["pk"]).device
        relay=self.queryset.get(pk=kwargs["pk"])
        answer =ralay_for_device_update(relay,device)
        if answer[0] == True:
            PMI.send_message(device.auth.mac_addres,answer[1])
        else:
            relay.enable = False
            relay.save()  
            return Response({"error":"You cannot activate a relay that you did not enter in the pins "},
                                status=status.HTTP_400_BAD_REQUEST)
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

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        queryset = queryset.filter(device__user=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        result = super().list(request, *args, **kwargs)
        return result


    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        sensor = SensorForDevice.objects.get(pk=kwargs["pk"])
        device_pin = sensor.device.pinofdevice
        sensor_id = "sensor_" +str(sensor.pk)
        print("\n\n\n\n\n Amad TO TABE no if")
        if sensor_id in device_pin.pin.values():
            print("\n\n\n\n\n Amad TO TABE")
            for pin_pk, sensor_pk in device_pin.pin.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
                print("\n\n\n\n\n ",pin_pk, sensor_pk)
                if sensor_pk == sensor_id:   
                    device_pin.pin[pin_pk]=None
            device_pin.save()
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
        queryset = queryset.filter(device__user=self.request.user)
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
                    relay =None
                    if split_key[0] not in ["sensor","relay"]:
                        return Response({'error': f"A sensor {key} not good format (sensor_pk | relay_pk) "}, status=status.HTTP_400_BAD_REQUEST)
                    if split_key[0]=="sensor":
                        sensor = device.device_sensor.get(pk=split_key[1]).sensor
                    else:
                        relay = device.device_relay.get(pk=split_key[1]).relay
                    if sensor != None and value != sensor.pin_number :
                        return Response({'error': f"A sensor {sensor.uniq_name} has {sensor.pin_number} pins while you have given {sensor}"}, status=status.HTTP_400_BAD_REQUEST)
                    elif relay !=None and value != 1:
                        return Response({'error': f"A relay can just one pins"}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'error': f"Use the corresponding device sensors for all pins"}, status=status.HTTP_400_BAD_REQUEST)
        PinFdevice = super().update(request, *args, **kwargs)
        device=self.queryset.get(pk=kwargs["pk"]).device
        if device.auth.mac_addres is not None:
            PMI.send_message(device.auth.mac_addres,pin_and_sensor_of_device(device))
        return PinFdevice



# class TimeDefualtValueViewSet(ModelViewSet):
#     queryset = TimeEnable.objects.all()
#     serializer_class =  TimeEnableSerializer
#     http_method_names = ['post' , 'get', 'delete', 'put']
#     # search_fields = ('uniq_name')

#     def __init__(self, **kwargs) -> None:
#         super().__init__(**kwargs)

#     def list(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)

#     def update(self, request, *args, **kwargs):
#         all_time=self.queryset.filter(sensorfordevice=kwargs["sensorfordevice"])
#         if (kwargs["end_day"] != None and kwargs["start_day"] < kwargs["end_day"]) or (kwargs["end_time"] != None and kwargs["start_time"] < kwargs["end_time"]):
#             pass
#         for time_check in all_time:          
#             if kwargs["start_day"] != None and kwargs["end_day"] != None and\
#                     time_check.start_day != None and time_check.start_day != None and  \
#                     (time_check.start_day < d2.start_day < time_check.end_day) or (time_check.start_day < d2.end_day < time_check.end_day) or (d2.start_day <= time_check.start_day and d2.end_day >= time_check.end_day):       
#                 if kwargs["start_time"] != None and kwargs["end_time"] != None and\
#                     time_check.start_time != None and time_check.start_time != None and  \
#                     (time_check.start_time < d2.start_time < time_check.end_time) or (time_check.start_time < d2.end_time < time_check.end_time) or (d2.start_time <= time_check.start_time and d2.end_time >= time_check.end_time):
#                     raise ValidationError()  
#         return super().update(request, *args, **kwargs)
    


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




@api_view(['GET'])
def sensorvalue(request,device,sensore=None):
    try:
        if device.isdigit():
            obj_device = Device.objects.get(pk=device)
        else:
            obj_device = Device.objects.get(name=device)

        senosr_list=[]
        rs=redisclient.query(f"select * from {obj_device.name}")
        respons ={"device":obj_device.name,"data":{}}
        if sensore is not None:
            senosr_list.extend(list(rs.get_points(tags={"sensor_id": f"{sensore}"})))
        else:
            senosr=obj_device.device_sensor.all()
            for sen in senosr:
                print(rs.get_points(tags={"sensor_id": f"{sen.pk}"}))
                senosr_list=senosr_list + list(rs.get_points(tags={"sensor_id": f"{sen.pk}"}))
                    
        for value in senosr_list[-20:]:
            tempjson={
                        "sensor_id":value.pop('sensor_id',None),
                        "time":value.pop('time',None),
                        "models":value.pop('models',None),
                        "sensor":value.pop('sensor',None),
                        "data":value,
                    }
            sensor = obj_device.device_sensor.get(pk=tempjson["sensor_id"]).sensor
            if tempjson["sensor_id"] is not None and tempjson["sensor_id"] not in respons["data"].keys() :
                respons["data"][tempjson["sensor_id"]]= [{
                    "time":tempjson['time'],
                    "value":tempjson["data"],
                }]  
            else:
                respons["data"][tempjson["sensor_id"]].append({
                    "time":tempjson['time'],
                    "value":tempjson["data"],
                })
                
        return Response(data=respons)
    except Exception as e:
        print("salam",e, e.__traceback__.tb_lineno )
        return Response({'error': f"not exit device or senore by id entered"}, status=status.HTTP_400_BAD_REQUEST)




class TimeActionViewSet(ModelViewSet):
    queryset = PeriodicTask.objects.all()
    serializer_class =  PeriodicTaskSerializer
    http_method_names = ['post' , 'get', 'delete', 'put']
    # permission_classes =(IsAdminUser,)
    # def filter_queryset(self, queryset):
    #     queryset = super().filter_queryset(queryset)
    #     queryset = queryset.filter(relay__device__user=self.request.user)
    #     return queryset
    

celery_app = current_app
def tasks_as_choices():
    print("celery_app",celery_app,"\n\n\n",celery_app.__dict__,"\n\n\n",celery_app.tasks,"\n\n\n")
    tasks = list(sorted(name for name in celery_app.tasks
                        if not name.startswith('celery.')))
    tasts = json.dumps(tasks)
    return tasts
    

@api_view(['GET'])
def tasksname(request):
    try:
        return Response(data=tasks_as_choices())
    except Exception as e:
        print("salam",e, e.__traceback__.tb_lineno )
        return Response({'error': f"not exit device or senore by id entered"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_device_token(request,device_id):
    try:
        device = Device.objects.get(pk=device_id)
        if  request.user == device.user:
            res_data = {
                "auth_token" : str(device.auth.token),
                "mac_addres" : str(device.auth.mac_addres)

            }
            return Response(data=res_data)
        else:
            return Response(data={"error":"not accsses to get token for entered device"})
    except Exception as e:
        return Response({'error': f"not exit device  by id entered"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def run_task_action(request):
    try:
        device = Device.objects.get(pk=request.POST.get("device_id"))
        relay_action={
            "type": "Action",
            "value": [
                {
                "id": request.POST.get("relay_pin"),
                "set": True if "True" in request.POST.get("status") else False,
                }
            ]
        }
        print("\n\n\n",str(device.auth.mac_addres),json.dumps(relay_action))
        PMI.send_message(str(device.auth.mac_addres),json.dumps(relay_action))
        return Response(data={"status":"ok",})
    except Exception as e:
        return Response({'error': f"not exit device  by id entered"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def send_data_in_websocket(request):
    channel_layer=get_channel_layer()
    group_name= request.POST.get("chat_id")
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_response',
            'message': str(request.POST.get("message"))
        }
    )
    return Response(data={"status":"ok",})

