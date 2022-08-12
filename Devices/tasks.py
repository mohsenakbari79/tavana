from celery import shared_task 
from time import sleep
from Devices.amqp import PMI
from Devices.models import Device

@shared_task(name="enable")
def mytaskenable(device_id,relay_pin):
    print("\n\n\ntask omad\n\n\n")
    try: 
        if relay_pin.isdigit() or "relay" not in relay_pin:
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
        PMI.send_message(str(device.auth.mac_addres),json.dumps(relay_action))
    except Exception as e:
        print("\n\n\n\n Task Error :::",e,"\n")

@shared_task(name="disable")
def mytaskenable(device_id,relay_pin):
    if relay_pin.isdigit() or "relay" not in relay_pin:
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
    PMI.send_message(str(device.auth.mac_addres),json.dumps(relay_action))
