from celery import shared_task 
from time import sleep
from Devices.amqp import PMI
from Devices.models import Device
import requests as re
import json
@shared_task(name="enable")
def mytaskenable(device_id,relay_pin):
    try:
        print("relay_pin.",relay_pin)
        relay_pin = str(relay_pin)
        if relay_pin.isdigit() or "relay" not in relay_pin:
            relay_pin= "relay_" + relay_pin
        print("relay+pin2",relay_pin,device_id)
        data={
                "relay_pin":relay_pin,
                "device_id":device_id,
                "status":True,
                }
        re.post("http://giahino:8000/api/task/action/",data=data)
        #PMI.send_message(str(device.auth.mac_addres),json.dumps(relay_action))
    except Exception as e:
        print(e)

@shared_task(name="disable")
def mytaskenable(device_id,relay_pin):
    try:
        relay_pin = str(relay_pin)
        if relay_pin.isdigit() or "relay" not in relay_pin:
            relay_pin= "relay_" + relay_pin
        data={
                "relay_pin":relay_pin,
                "device_id":device_id,
                "status":False,
                }
        re.post("http://giahino:8000/api/task/action/",data=data)
    except Exception as e:
        print(e)


