import json
from unicodedata import name
from Devices.models import Device,Sensor,SensorForDevice
from collections import defaultdict
from influxdb import InfluxDBClient
from datetime import datetime
from decouple import config
#Setup database
redisclient = InfluxDBClient("influxdb", 8086, 'admin', 'Password1')
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


# def sensor_value(device:object,id_sensor:int,body:json):
#     sensorvaluecheck=True
#     sensor=device.device_sensor.get(pk=id_sensor).sensor
#     sensor_vlaue=sensor.sensorvaluetype
#     if sensor_vlaue.types == "STR":
#         json_payload = [] 
#         for data in  body.get("data"):
#             if data in sensor.validation.get("key_porblem",[]):
#                 pass
#             else: 
#                 data = {
#                     "measurement":device.name ,
#                     "tags": {
#                         "sensor":sensor.name,
#                         "sensor_value":sensor.pk
#                         },
#                     "time": datetime.now(),
#                     "fields": {
#                         'data': data,
#                     } 

#                 }
#                 json_payload.append(data)

#     elif sensor_vlaue.types == "INT":
#         min_v = sensor.validation.get("min_value") if sensor.validation.get("min_value").isdigit() else float("-inf")
#         max_v = sensor.validation.get("max_value") if sensor.validation.get("max_value").isdigit() else float("inf")
#         for data in  body.get("data"): 
#             if  min_v< data < max_v :
#                 data = {
#                     "measurement":device.name ,
#                     "tags": {
#                         "sensor_id":sensor_vlaue.pk
#                         },
#                     "time": datetime.now(),
#                     "fields": {
#                         'data': data,
#                     } 

#                 }
#                 json_payload.append(data)
#             else:
#                 pass
#     redisclient.write_points(json_payload)


def sensor_value(device:object,id_sensor:int,body:json):
    sensorvaluecheck=True
    sensor_device=device.device_sensor.get(pk=id_sensor)
    sensor_vlaues=sensor_device.sensor.SensorValueType.all().sorted()
    len_device=sensor_values.count()
    for index,sensor_vlaue in enumerate(sensor_vlaues):
        if sensor_vlaue.types == "STR":
            json_payload = [] 
            for data in  body.get("values",{}).get("data",[])[index::len_device]:
                validation=sensor_device.sensorvalidation.all()
                for valid in validation:
                    if data in valid.validation.get("key_porblem",[]):
                        pass

                data = {
                            "measurement":device.name ,
                            "tags": {
                                "sensor":sensor_device.sensor.uniq_name,
                                "sensor_value":sensor_device.pk
                                },
                            "time": datetime.now(),
                            "fields": {
                                str(sensor_vlaue.name): data,
                            } 

                        }
                        json_payload.append(data)

        elif sensor_vlaue.types == "INT":
            for data in  body.get("values",{}).get("data",[])[index::len_device]: 
                validation=sensor_device.sensorvalidation.all()
                for valid in validation:
                    min_v = valid.validation.get("min_value") if valid.validation.get("min_value").isdigit() else float("-inf")
                    max_v = valid.validation.get("max_value") if valid.validation.get("max_value").isdigit() else float("inf")
                    if not(min_v< data < max_v):
                        pass
                data = {
                        "measurement":device.name ,
                        "tags": {
                            "sensor_id":sensor_vlaue.pk
                            },
                        "time": datetime.now(),
                        "fields": {
                            str(sensor_vlaue.name): data,
                        } 

                    }
                json_payload.append(data)
    redisclient.write_points(json_payload)
    if sensorvaluecheck:
        pin_and_sensor_of_device()
 


def pin_and_sensor_of_device(device:object):
    pin = device.pinofdevice.pin
    res = defaultdict(list)
    senosr = device.device_sensor.all()
    relay = device.

    respons={
        "type" : "Sensor",
        "value" : [] ,
    }
    for key, val in sorted(pin.items()):
        if val != None:
            res[val].append(key)
    for sensor_rele ,value in res.items():
        splitsensor_rele=sensor_rele.split("_")
        if splitsensor_rele[0]=="sensor"
            respons["value"].append({
                "id": sensor_rele,
                "name": senosr.get(pk=splitsensor_rele[1]).sensor.uniq_name,
                "pins": value,
                "active":senosr.get(pk=splitsensor_rele[1]).enable
            })
        else splitsensor_rele[0]=="relay"
            respons["value"].append({
                "id": sensor_rele,
                "name": senosr.get(pk=splitsensor_rele[1]).sensor.uniq_name,
                "pins": value,
                "active":senosr.get(pk=splitsensor_rele[1]).enable
            })
    return json.dumps(respons)
     
