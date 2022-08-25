from channels.generic.websocket import JsonWebsocketConsumer, AsyncJsonWebsocketConsumer
# from channels.exceptions import StopConsumer
# from asgiref.sync import async_to_sync
import json
import requests
from Devices.amqp import PMI

# models
from Devices.models import Device






class DeviceJsonData(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        try:
            self.sensor_id = self.scope['url_route']['kwargs']['sensorId']
            self.device_id = self.scope['url_route']['kwargs']['deviceId']
            device_temp = Device.objects.filter(pk=self.device_id )
            
            if device_temp.exists():
                self.device = device_temp.first()
                temp_sensor = self.device.device_sensor.filter(pk = self.sensor_id )
                if not temp_sensor.exists():
                    await self.close(404)
                if temp_sensor.first().sensor.mutualـcommunication:
                    await self.close(400)
            else :
                await self.close(404)
            if 'user' not in self.scope:
                await self.close(403)
            elif self.scope['user'].is_anonymous:
                await self.close(403)
            else:
                await self.accept()
                await self.channel_layer.group_add(
                    f"{self.device_id}_{self.sensor_id}",
                    self.channel_name,
                )
        except Exception as e:
            print("CONNECT ERROR",e)
            await self.close(403)


        event = {'type': 'send_data'}
        

    async def disconnect(self, close_code):
        print(f"close connect web socket :) status code ={close_code} ")
    async def receive_json(self, content, **kwargs):
        
        content["chat_id"] = f"{self.device_id}_{self.sensor_id}"
        content["id"] = f"sensor_{self.sensor_id}"
        temp = {
                "type": "Input",
                "value": content
                } 
        print("receive",content,self.device.auth.mac_addres,temp)

        PMI.send_message(str(self.device.auth.mac_addres),json.dumps(temp))
        
    async def send_response(self, data):
        print(data,"sendrespnese")
        await self.send_json(data)
    

    # def send_data(self, event):
    #     pass

