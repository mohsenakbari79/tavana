import json
from unicodedata import name
from Devices.models import Device,Sensor,SensorForDevice
from collections import defaultdict
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


def sensor_value(device:object,id_sensor:int,body:json):
    sensor=device.sensor.get(pk=id_sensor)
    if sensor.types == "STR":
        for data in  body.get("data"):
            if data in sensor.validation.get("key_porblem",[]):
                pass
            else:
                pass
                # TODO : save in infux db
    elif sensor.types == "INT":
        min_v = sensor.validation.get("min_value") if sensor.validation.get("min_value").isdigit() else float("-inf")
        max_v = sensor.validation.get("max_value") if sensor.validation.get("max_value").isdigit() else float("inf")
        for data in  body.get("data"): 
            if  min_v< data < max_v :
                pass
                # TODO : save in infux db
            else:
                pass 
def pin_and_sensor_of_device(device:object):
    pin = device.pinofdevice.pin
    res = defaultdict(list)
    respons={
        "type" : "Sensor",
        "value" : [] ,
    }
    for key, val in sorted(pin.items()):
        if val != None:
            res[val].append(key)
    for sensor ,value in res.items():
        respons["value"].append({
            "id": sensor,
            "name": Sensor.objects.get(pk=sensor).uniq_name,
            "pins": value,
            "active":"enable"
        })
    return json.dumps(respons)
     