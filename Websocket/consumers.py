from channels.generic.websocket import JsonWebsocketConsumer, AsyncJsonWebsocketConsumer
# from channels.exceptions import StopConsumer
# from asgiref.sync import async_to_sync
import json
import requests
from Devices.amqp import PMI
#CONTROLLER_ADDR="192.168.5.195"






class DeviceJsonData(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        self.sensor_id = self.scope['url_route']['kwargs']['sensorId']
        self.device_id = self.scope['url_route']['kwargs']['deviceId']
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


        event = {'type': 'send_data'}
        

    async def disconnect(self, close_code):
        print(f"close connect web socket :) status code ={close_code} ")
    async def receive_json(self, content, **kwargs):
        content["chat_id"] = f"{self.device_id}_{self.sensor_id}"
        content["id"] = f"sensor_{self.sensor_id}"
        temp = {
                "type": "Output",
                "value": content
                } 

        PMI.send_message(method.routing_key,temp)
        
    async def send_response(self, data):
        await self.send_json(data)
    

    # def send_data(self, event):
    #     pass

