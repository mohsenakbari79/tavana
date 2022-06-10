from easy_pika.pika_obj import PikaMassenger
import json 
import redis
from redis.commands.json.path import Path
import threading

from Devices.models import Device,SensorForDevice,Sensor
from Devices.utils import add_sensor_to_device
# client = redis.Redis(host='localhost', port=6379, db=0)
# result = client.json().get('somejson:1')


PMI=PikaMassenger(host='localhost',port=5672,username='guest',password='guest',exchange_name="Message2")
def callback(ch, method, properties, body):
    try:
        device=Device.objects.get(name=properties.headers['DeviceNameU'])
        body=json.loads(body)
        if method.routing_key=="sensore":
            add_sensor_to_device(device.pk,body['value'])
        elif "sensor_value" in method.routing_key.lower():
            sensor_name=method.routing_key.split("_")[1]
            sensor=Sensor.objects.get(uniq_name=sensor_name)
            sensorFdevice=SensorForDevice.objects.get(sensor=sensor,device=device)
            for key,value in body.items():
                sensorFdevice.value[key] =sensorFdevice.value.get(key,[]).append(value)
            sensorFdevice.save() 
        elif "enable_sensore" in method.routing_key.lower():
            sensor_name=method.routing_key.split("_")[1]
            sensor=Sensor.objects.get(uniq_name=sensor_name)
            sensorFdevice=SensorForDevice.objects.get(sensor=sensor,device=device)
            sensorFdevice.enable=body.get("status",)
    except:
        pass
    PMI.connection._channel.basic_ack(method.delivery_tag)
    # client.json().set(json.loads(body))


test1=threading.Thread(name="test" , target=PMI.run ,kwargs={'queue_name':"shire",'routing_keys':["device","sensore",],'callback':callback})


