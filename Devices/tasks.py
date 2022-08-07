from celery import shared_task 
from time import sleep
from Devices.amqp import PMI
from Devices.models import Device
import paho.mqtt.publish as publish
from decouple import config


@shared_task(name="enable")
def mytaskenable(device_id,relay_pin):
    print("device_id,relay_pin",device_id,relay_pin)
    if "relay" not in relay_pin and relay_pin.isdigit():
        relay_pin= "relay_"+str(relay_pin)
    device = Device.objects.get(pk=device_id)
    relay_action={
            "type": "Action",
            "value": [
                {
                "id": relay_pin,
                "set": True,
                }
            ]
        }
    print("device.auth.mac_addres",device.auth.mac_addres,relay_action)
    publish.single(topic=device.auth.mac_addres, payload=json.dumps(relay_action), hostname=config('HOSTSERVER'),auth={"username":device.auth.mac_addres,"password":device.auth.token})



@shared_task(name="disable")
def mytaskenable(device_id,relay_pin):
    if "relay" not in relay_pin and relay_pin.isdigit():
        relay_pin= "relay_"+str(relay_pin)
    device = Device.objects.get(pk=device_id)
    relay_action={
            "type": "Action",
            "value": [
                {
                "id": relay_pin,
                }
            ]
        }
    publish.single(topic=device.auth.mac_addres, payload=json.dumps(relay_action), hostname=config('HOSTSERVER'),auth={"username":device.auth.mac_addres,"password":device.auth.token})
