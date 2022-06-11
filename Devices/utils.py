import json
from unicodedata import name
from Devices.models import Device,Sensor,SensorForDevice

def add_sensor(listsernsor:list): 
    if len(listsernsor):
        for name_sensor in  listsernsor:
            sensor=Sensor.objects.get_or_create(uniq_name=name_sensor)
            sensor[0].save()
    return None
def add_sensor_to_device(deviceid:int,listsernsor:list) ->bool:
    device=Device.objects.get(pk=deviceid)
    try:
        for name_sensor in  listsernsor:
            sensor=Sensor.objects.get_or_create(uniq_name=name_sensor)
            sensorfordevice=SensorForDevice.objects.get_or_create(sensor=sensor,device=device)
            sensor.save()
            sensorfordevice.save()
    except:
        pass


def sensor_value(sensor_name:str,device:object,body:json):
    sensor=Sensor.objects.get(uniq_name=sensor_name)
    sensorFdevice=SensorForDevice.objects.get(sensor=sensor,device=device)
    for key,value in body.items():
        sensorFdevice.value[key] =sensorFdevice.value.get(key,[]).append(value)
    sensorFdevice.save() 