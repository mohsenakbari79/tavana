import json
from unicodedata import name
from Devices.models import Device,Sensor,SensorForDevice
from collections import defaultdict
from influxdb import InfluxDBClient
from datetime import datetime
from decouple import config
#Setup database
redisclient = InfluxDBClient("localhost", 8086, 'admin', 'Password1')
redisclient.create_database('mydb')
redisclient.switch_database('mydb')

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
    sensorvaluecheck=True
    sensor=device.device_sensor.get(pk=id_sensor).sensor
    sensor_vlaue=sensor.sensorvaluetype
    if sensor_vlaue.types == "STR":
        json_payload = [] 
        for data in  body.get("data"):
            if data in sensor.validation.get("key_porblem",[]):
                pass
            else: 
                data = {
                    "measurement":device.name ,
                    "tags": {
                        "sensor":sensor.name,
                        "sensor_value":sensor.pk
                        },
                    "time": datetime.now(),
                    "fields": {
                        'data': data,
                    } 

                }
                json_payload.append(data)

    elif sensor_vlaue.types == "INT":
        min_v = sensor.validation.get("min_value") if sensor.validation.get("min_value").isdigit() else float("-inf")
        max_v = sensor.validation.get("max_value") if sensor.validation.get("max_value").isdigit() else float("inf")
        for data in  body.get("data"): 
            if  min_v< data < max_v :
                data = {
                    "measurement":device.name ,
                    "tags": {
                        "sensor_id":sensor_vlaue.pk
                        },
                    "time": datetime.now(),
                    "fields": {
                        'data': data,
                    } 

                }
                json_payload.append(data)
            else:
                pass
    redisclient.write_points(json_payload)
    # if sensorvaluecheck:
    #     pin_and_sensor_of_device()
 
def pin_and_sensor_of_device(device:object):
    pin = device.pinofdevice.pin
    res = defaultdict(list)
    senosr = device.device_sensor.all()
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
            "name": senosr.get(pk=sensor).sensor.uniq_name,
            "pins": value,
            "active":senosr.get(pk=sensor).enable
        })
    return json.dumps(respons)
     