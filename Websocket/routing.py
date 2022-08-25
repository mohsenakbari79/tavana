from django.urls import path
from Websocket import consumers


websocket_urlpatterns = [
    path('ws/test/<str:deviceId>/<str:sensorId>/', consumers.DeviceJsonData.as_asgi()),
]
